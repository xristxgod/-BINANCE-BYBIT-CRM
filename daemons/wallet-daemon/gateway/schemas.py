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
    fee: str
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
