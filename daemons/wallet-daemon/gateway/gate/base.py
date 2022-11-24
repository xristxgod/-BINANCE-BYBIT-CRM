import os
import abc
import decimal
from typing import NoReturn, Type, Optional, List

import aiofiles

import meta
import src.settings as settings
import gateway.logger as logger
from gateway.schemas import BlockSchema, TransactionSchema, RawTransaction


class AbstractNode:
    network_name: str
    endpoint_uri: str

    class SmartContract(abc.ABC):
        @abc.abstractclassmethod
        async def connect(cls, address: str): ...

    @property
    def network(self) -> str:
        return self.network

    @abc.abstractmethod
    async def get_block(self, block_number: int) -> BlockSchema: ...

    @abc.abstractmethod
    async def get_latest_block_number(self) -> int: ...

    @abc.abstractmethod
    async def get_balance(self, address: str, token: Optional[str] = None) -> decimal.Decimal: ...

    @abc.abstractmethod
    async def create_transaction(
            self, from_: str, to: str, amount: decimal.Decimal, token: Optional[str] = None
    ) -> RawTransaction: ...

    @abc.abstractmethod
    async def sing_transaction(self, raw_data: str, private_key: str) -> str: ...

    @abc.abstractmethod
    async def send_transaction(self, raw_transaction: str) -> TransactionSchema: ...


class DefaultBlockManager:
    class FileBlockManager:

        def __init__(self, name: str):
            self.file_path = os.path.join(settings.BLOCKS_DIR, f'{name}_block.txt')

        async def write(self, block_number: int) -> NoReturn:
            async with aiofiles.open(self.file_path, 'w', encoding='utf-8') as file:
                await file.write(str(block_number))

        async def read(self) -> str:
            async with aiofiles.open(self.file_path, "r", encoding='utf-8') as file:
                return await file.read()

    __slots__ = (
        '__node', 'manager'
    )

    def __init__(self, node: AbstractNode):
        self.__node = node
        self.manager = self.FileBlockManager(name=self.__node.network)

    async def get_block_by_id(self, block_number: int) -> BlockSchema:
        return await self.__node.get_block(block_number)

    async def get_latest_block_number(self) -> int:
        return await self.__node.get_latest_block_number()

    # Daemon function

    async def get_block_in_storage(self) -> int:
        block_number = await self.manager.read()
        if block_number:
            return int(block_number)
        return await self.get_latest_block_number()

    async def save_block_to_storage(self, block: int) -> NoReturn:
        return await self.manager.write(block_number=block)


class DefaultTransactionManager:
    __slots__ = (
        'logger', '__node'
    )

    def __init__(self, node: AbstractNode, cls_logger: Type):
        self.logger = cls_logger()
        self.__node = node

    async def create_transaction(self, from_: str, to: str, amount: decimal.Decimal):
        pass

    async def send_transaction(self, transaction_hash: str, private_key: str) -> TransactionSchema:
        pass

    async def get_transaction_by_transaction_id(self, transaction_id: str) -> TransactionSchema:
        pass

    async def get_transactions_by_wallet_address(self, address: str) -> List[TransactionSchema]:
        pass


class DefaultWalletManager:
    __slots__ = (
        'logger', '__node'
    )

    def __init__(self, node: AbstractNode, cls_logger: Type):
        self.logger = cls_logger()
        self.__node = node

    async def get_balance(self, address: str, token: str) -> decimal.Decimal:
        return await self.__node.get_balance(address=address, token=token)

    async def get_optimal_fee(self, from_: str, to: str, amount: decimal.Decimal) -> decimal.Decimal:
        pass


class BaseGateClient:
    cls_node: Type[AbstractNode]

    block_manager: Type[DefaultBlockManager] = DefaultBlockManager
    transaction_manager: Type[DefaultTransactionManager] = DefaultTransactionManager
    wallet_manager: Type[DefaultWalletManager] = DefaultWalletManager

    __slots__ = (
        '__node_manager', '__block_manager',
        '__transaction_manager', '__wallet_manager'
    )

    def __init__(self, **kwargs):
        self.__node_manager = self.cls_node()

        self.logger = self.__get_logger(self.__node_manager.network)

        self.__block_manager = self.block_manager(node=self.__node_manager)
        self.__transaction_manager = self.transaction_manager(node=self.__node_manager, cls_logger=self.logger)
        self.__wallet_manager = self.wallet_manager(node=self.__node_manager, cls_logger=self.logger)
    
    @classmethod
    def __get_logger(cls, network: str = 'base') -> Type:
        return type(
            f'{network.title()}GateClientLogger',
            (logger.meta.Logger,), 
            {'path': f'{network.lower()}_gate_logger.log'}
        )

    def block(self) -> DefaultBlockManager:
        return self.__block_manager

    def transaction(self) -> DefaultTransactionManager:
        return self.__transaction_manager

    def wallet(self) -> DefaultWalletManager:
        return self.__wallet_manager

    def node(self) -> AbstractNode:
        return self.__node_manager


__all__ = [
    'BaseGateClient',
    'AbstractNode'
]
