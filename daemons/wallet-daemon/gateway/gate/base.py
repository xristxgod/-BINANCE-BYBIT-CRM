import os
import decimal
from typing import NoReturn, Type, Optional, List

import aiofiles

import meta
import settings as settings
from src.schemas import BlockSchema, TransactionSchema, RawTransaction
from src.abstract import AbstractNode


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

    async def create_transaction(
            self, from_: str, to: str, amount: decimal.Decimal, token: Optional[str] = None
    ) -> RawTransaction:
        self.logger.log('{} :: Create transaction :: Data: {} :: Token: {}'.format(
            self.__class__.__name__, {'form': from_, 'to': to, 'amount': amount}, token if token else 'Native'
        ))
        return await self.__node.create_transaction(from_, to, amount=amount)

    async def send_transaction(self, raw_data: str, private_key: str) -> TransactionSchema:
        self.logger.log('{} :: Send transaction :: Sign :: Raw data: {}'.format(
            self.__class__.__name__, raw_data
        ))
        raw_transaction = await self.__node.sign_transaction(raw_data=raw_data, private_key=private_key)
        self.logger.log('{} :: Send transaction :: Send :: Raw Transaction: {}'.format(
            self.__class__.__name__, raw_data
        ))
        return await self.__node.send_transaction(raw_transaction=raw_transaction)

    async def get_transaction_by_transaction_id(self, transaction_id: str) -> TransactionSchema:
        return await self.__node.get_transaction(transaction_id=transaction_id)

    async def get_transactions_by_wallet_address(self, address: str) -> List[TransactionSchema]:
        return await self.__node.get_transactions_by_address(address=address)


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
        raw_transaction = await self.__node.create_transaction(from_, to, amount=amount)
        return raw_transaction.fee


class GateClient:
    block_manager: Type[DefaultBlockManager] = DefaultBlockManager
    transaction_manager: Type[DefaultTransactionManager] = DefaultTransactionManager
    wallet_manager: Type[DefaultWalletManager] = DefaultWalletManager

    __slots__ = (
        '__node_manager', '__block_manager',
        '__transaction_manager', '__wallet_manager'
    )

    def __init__(self, logger, node: Type[AbstractNode], **kwargs):
        self.__node_manager = node()

        self.__block_manager = self.block_manager(node=self.__node_manager)
        self.__transaction_manager = self.transaction_manager(node=self.__node_manager, cls_logger=logger)
        self.__wallet_manager = self.wallet_manager(node=self.__node_manager, cls_logger=logger)

    @property
    def block(self) -> DefaultBlockManager:
        return self.__block_manager

    @property
    def transaction(self) -> DefaultTransactionManager:
        return self.__transaction_manager

    @property
    def wallet(self) -> DefaultWalletManager:
        return self.__wallet_manager

    @property
    def node(self) -> AbstractNode:
        return self.__node_manager


class BaseGateway:
    cls_node: Type[AbstractNode]

    def __init__(self, logger=None):
        if logger is None:
            logger = meta.get_logger(self.__class__.__name__)
        self.logger = logger

        self.client = GateClient(logger=self.logger, node=self.cls_node)

    @property
    def gate(self) -> GateClient:
        return self.client


__all__ = [
    'GateClient',
    'BaseGateway',
    'AbstractNode'
]
