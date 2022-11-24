import decimal
import uuid

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

import core.base.enums as enums
from core.credential_manager import WalletCredentialManager, WalletCredential


class Network(models.Model):
    name = models.CharField(_('Network name'), max_length=25, primary_key=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('Network')
        verbose_name_plural = _('Networks')


class Token(models.Model):
    name = models.CharField(_('Token name'), max_length=25)
    symbol = models.CharField(_('Token symbol'), max_length=25)
    token_address = models.CharField(
        _('Token address'), max_length=255,
        default=None, null=True,
        blank=True, unique=True
    )

    decimals = models.IntegerField(_('Decimals'), default=8)
    extra = models.JSONField(_('Extra'), default=None, null=True, blank=True)

    network = models.ForeignKey(
        Network,
        related_name='token_network',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.network} :: {self.name}'

    class Meta:
        verbose_name = _('Token')
        verbose_name_plural = _('Token')


class Wallet(models.Model):
    address: str = models.CharField(_('Wallet address'), max_length=255, primary_key=True, validators=[])
    network = models.ForeignKey(
        Network,
        related_name='wallet_network',
        on_delete=models.CASCADE
    )

    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True)

    active = models.BooleanField(_('Active'), default=True)

    user: AbstractUser = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='user_crypto_wallet',
        on_delete=models.CASCADE
    )

    @property
    def private_key(self) -> WalletCredential:
        return WalletCredentialManager.get(self.address)

    @private_key.setter
    def private_key(self, keys: WalletCredential):
        WalletCredentialManager.set(self.address, keys=keys)

    @private_key.deleter
    def private_key(self):
        WalletCredentialManager.remove(self.address)

    def __str__(self):
        return f'Wallet {self.pk} :: {self.network}'

    class Meta:
        verbose_name = _('Wallet')
        verbose_name_plural = _('Wallets')


class Balance(models.Model):
    amount = models.DecimalField(_('Amount'), max_digits=8, decimal_places=8, default=0)
    token = models.ForeignKey(
        Network,
        related_name='balance_token',
        on_delete=models.CASCADE
    )

    active = models.BooleanField(_('Active'), default=True)

    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True)

    user: AbstractUser = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='user_crypto_wallet_balance',
        on_delete=models.CASCADE
    )
    wallet = models.ForeignKey(
        Wallet,
        related_name='wallet_balance',
        on_delete=models.CASCADE
    )

    @property
    def balance(self) -> decimal.Decimal:
        return self.amount

    @balance.setter
    def balance(self, balance: decimal.Decimal):
        self.amount = balance

    @property
    def balance_usd(self) -> str:
        raise NotImplementedError

    def __str__(self):
        return f'Balance: {self.pk}'

    class Meta:
        verbose_name = _('Balance')
        verbose_name_plural = _('Balances')


class ExternalTransactions(models.Model):
    transaction_id = models.CharField(_('Transaction ID'), max_length=255, primary_key=True)

    address = models.CharField(_('From Wallet address'), max_length=255)

    amount = models.DecimalField(_('Amount'), max_digits=18, decimal_places=6, default=0)
    fee = models.DecimalField(_('Commission'), max_digits=18, decimal_places=6, default=0)

    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True)

    type = models.CharField(
        _('User type'),
        max_length=50,
        choices=enums.ExternalTransactionType.choices,
        default=enums.ExternalTransactionType.RECIPIENT
    )

    token = models.ForeignKey(
        Network,
        related_name='external_transaction_token',
        on_delete=models.CASCADE
    )

    user: AbstractUser = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='user_crypto_external_transaction',
        on_delete=models.CASCADE
    )
    wallet = models.ForeignKey(
        Wallet,
        related_name='wallet_external_transaction',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'Transaction: {self.transaction_id}'

    class Meta:
        verbose_name = _('External Transaction')
        verbose_name_plural = _('External Transactions')


class InternalTransaction(models.Model):
    transaction_id = models.UUIDField(_('Internal transaction ID'), default=uuid.uuid4(), primary_key=True)

    sender = models.ForeignKey(
        Wallet,
        default=None,
        related_name='sender_wallet_crypto_internal_transaction',
        on_delete=models.SET_DEFAULT
    )
    recipient = models.ForeignKey(
        Wallet,
        default=None,
        related_name='recipient_wallet_crypto_internal_transaction',
        on_delete=models.SET_DEFAULT
    )

    amount = models.DecimalField(_('Amount'), max_digits=18, decimal_places=6, default=0)
    fee = models.DecimalField(_('Commission'), max_digits=18, decimal_places=6, default=0)

    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True)

    def __str__(self):
        return f'Transaction: {self.transaction_id}'

    class Meta:
        verbose_name = _('Internal Transaction')
        verbose_name_plural = _('Internal Transactions')
