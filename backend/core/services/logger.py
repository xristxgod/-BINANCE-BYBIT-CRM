import os

import core.meta as meta
from mainapp.settings import LOGS_PATH


class AccountCredentialManagerLogger(meta.Logger):
    path = os.path.join(LOGS_PATH, 'account_credential_manager.log')


class WalletCredentialManagerLogger(meta.Logger):
    path = os.path.join(LOGS_PATH, 'account_credential_manager.log')
