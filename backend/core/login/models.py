import os
import binascii
from datetime import datetime, timedelta

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class AuthToken(models.Model):
    key = models.CharField(
        _('Token'),
        max_length=50,
        default=binascii.hexlify(os.urandom(20)).decode(),
        primary_key=True
    )
    user: AbstractUser = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='user_auth_token',
        on_delete=models.CASCADE
    )
    created: datetime = models.DateTimeField(_('Created'), auto_now_add=True)

    LIFETIME = timedelta(hours=24*30)

    def __str__(self):
        return f'{self.pk}'

    @property
    def expires(self) -> datetime:
        return self.created + self.LIFETIME

    @property
    def is_expired(self) -> bool:
        return timezone.now() > self.expires

    @classmethod
    def expired_qs(cls):
        return cls.objects.filter(created__lt=timezone.now() - cls.LIFETIME)

    class Meta:
        verbose_name = _('Auth token')
        verbose_name_plural = _('Auth tokens')
