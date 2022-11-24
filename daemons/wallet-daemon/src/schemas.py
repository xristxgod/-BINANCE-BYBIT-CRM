import decimal
from dataclasses import dataclass, field
from typing import Optional, List, Dict


@dataclass()
class BlockHeaderSchema:
    block: int
    timestamp: int


@dataclass()
class ParticipantSchema:
    address: str
    amount: decimal.Decimal


@dataclass()
class RawTransaction:
    rawData: str
    fee: decimal.Decimal
    extra: Dict = field(default_factory=dict)


@dataclass()
class TransactionSchema:
    transactionId: str
    amount: decimal.Decimal
    fee: decimal.Decimal
    inputs: List[ParticipantSchema]
    outputs: List[ParticipantSchema]
    timestamp: int
    token: Optional[str] = None


@dataclass()
class BlockSchema:
    headers: BlockHeaderSchema
    transactions: List[TransactionSchema]


@dataclass()
class MessageHeadersSchemas:
    network: str
    blockNumber: int
    timestamp: int


@dataclass()
class MessageSchemas:
    headers: MessageHeadersSchemas
    body: List[TransactionSchema]


@dataclass()
class BalancerThreadMessage:
    address: str
    token: Optional[str] = None
    extra: Dict = field(default_factory=dict)
