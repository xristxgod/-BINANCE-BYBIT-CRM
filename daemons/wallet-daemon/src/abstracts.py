import abc
import decimal
from typing import Optional, List

from src.schemas import TransactionSchema, BlockSchema, RawTransaction


class AbstractNode:
    network: str
    endpoint_uri: str

    class SmartContract:
        @classmethod
        async def connect(cls, address: str):
            raise NotImplementedError

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

    @abc.abstractmethod
    async def get_transaction(self, transaction_id: str) -> TransactionSchema: ...

    @abc.abstractmethod
    async def get_transactions_by_address(self, address: str) -> List[TransactionSchema]: ...


class AbstractSender:

    @abc.abstractmethod
    async def send(self):
        pass
