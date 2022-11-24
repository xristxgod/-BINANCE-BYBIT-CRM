import typing
from abc import ABC, abstractclassmethod


class AbstractCredentialManager(ABC):
    service_id: str

    @abstractclassmethod
    def set(cls, *args, **kwargs) -> typing.NoReturn: ...

    @abstractclassmethod
    def get(cls, *args, **kwargs) -> typing.Optional: ...

    @abstractclassmethod
    def remove(cls, account: str) -> typing.NoReturn: ...


__all__ = [
    'AbstractCredentialManager'
]
