import dataclasses
import json
import typing

import keyring

import core.credential_manager.base as base
from core.services.logger import WalletCredentialManagerLogger as Logger
from mainapp.settings import WALLET_CREDENTIAL_MANAGER_SERVICE_ID


@dataclasses.dataclass
class WalletCredential:
    privateKey: str


class WalletCredentialManager(base.AbstractCredentialManager):
    service_id = WALLET_CREDENTIAL_MANAGER_SERVICE_ID

    @classmethod
    def set(cls, address: str, *, keys: WalletCredential) -> typing.NoReturn:
        item = keyring.get_password(cls.service_id, address)
        if item is None:
            Logger.log('Wallet address: {} :: Set Private key'.format(address))
            keyring.set_password(
                cls.service_id,
                address,
                json.dumps(dataclasses.asdict(keys))
            )

    @classmethod
    def get(cls, address: str) -> typing.Optional[WalletCredential]:
        keys = keyring.get_password(cls.service_id, address)
        if keys is not None:
            Logger.log('Wallet address: {} :: Get Private key'.format(address))
            return WalletCredential(**json.loads(keys))

    @classmethod
    def remove(cls, address: str) -> typing.NoReturn:
        keys = keyring.get_password(cls.service_id, address)
        if keys is not None:
            Logger.log('Wallet address: {} :: Delete Private key'.format(address))
            keyring.delete_password(cls.service_id, address)


__all__ = [
    'WalletCredential',
    'WalletCredentialManager'
]
