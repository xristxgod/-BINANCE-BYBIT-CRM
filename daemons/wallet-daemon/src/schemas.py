import enum
from dataclasses import dataclass


class Network(enum.Enum):
    tron = 'TRON'


class Token(enum.Enum):
    native = 'NATIVE'
    usdt = 'USDT'


@dataclass()
class Wallet:
    address: str
