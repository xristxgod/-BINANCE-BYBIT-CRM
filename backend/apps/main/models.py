from typing import Optional

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

import core.base.enums as enums
from core.credential_manager import AccountCredentialManager, ApiCredential


class Google2FA(models.Model):
    code = models.CharField(_('2FA code'), max_length=25, primary_key=True)
    qr_code = models.CharField(_('2FA code for QR'), max_length=255, unique=True)

    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True)

    active = models.BooleanField(_('Active'), default=True)

    user: AbstractUser = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='user_2fa',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'Code: {self.code}'

    class Meta:
        verbose_name = _('Google 2FA code')
        verbose_name_plural = _('Google 2FA codes')


class Telegram(models.Model):
    chat_id = models.BigIntegerField(_('Telegram Chat ID'), primary_key=True)

    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True)

    active = models.BooleanField(_('Active'), default=True)

    user: AbstractUser = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='user_telegram',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'ID: {self.chat_id}'

    class Meta:
        verbose_name = _('Telegram code')
        verbose_name_plural = _('Telegram codes')


class Account(models.Model):
    name = models.CharField(_('Account name'), max_length=55, unique=True)
    network = models.CharField(
        _('Network'),
        max_length=20,
        choices=enums.AccountNetwork.choices,
        default=enums.AccountNetwork.BINANCE
    )

    active = models.BooleanField(_('Active'), default=True)

    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True)

    user: AbstractUser = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='user_account',
        on_delete=models.CASCADE
    )

    @property
    def api_name(self) -> str:
        return f'{self.network}@{self.name}'

    @property
    def api_keys(self) -> Optional[ApiCredential]:
        return AccountCredentialManager.get(account=self.api_name)

    @api_keys.setter
    def api_keys(self, keys: ApiCredential):
        AccountCredentialManager.set(self.api_name, keys=keys)

    @api_keys.deleter
    def api_keys(self):
        AccountCredentialManager.remove(account=self.api_name)

    def __str__(self):
        return f'{self.api_name}'

    class Meta:
        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')
