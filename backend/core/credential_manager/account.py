import dataclasses
import json
import typing

import keyring

import core.credential_manager.base as base
from core.services.logger import AccountCredentialManagerLogger as Logger
from mainapp.settings import ACCOUNT_CREDENTIAL_MANAGER_SERVICE_ID


@dataclasses.dataclass
class ApiCredential:
    apiKey: str
    secretKey: str


class AccountCredentialManager(base.AbstractCredentialManager):
    service_id = ACCOUNT_CREDENTIAL_MANAGER_SERVICE_ID

    @classmethod
    def set(cls, account: str, *, keys: ApiCredential) -> typing.NoReturn:
        item = keyring.get_password(cls.service_id, account)
        if item is None:
            Logger.log('Account: {} :: Set Keys'.format(account))
            keyring.set_password(
                cls.service_id,
                account,
                json.dumps(dataclasses.asdict(keys))
            )

    @classmethod
    def get(cls, account: str) -> typing.Optional[ApiCredential]:
        keys = keyring.get_password(cls.service_id, account)
        if keys is not None:
            Logger.log('Account: {} :: Get Keys'.format(account))
            return ApiCredential(**json.loads(keys))

    @classmethod
    def remove(cls, account: str) -> typing.NoReturn:
        keys = keyring.get_password(cls.service_id, account)
        if keys is not None:
            Logger.log('Account: {} :: Delete Keys'.format(account))
            keyring.delete_password(cls.service_id, account)


__all__ = [
    'ApiCredential',
    'AccountCredentialManager'
]
