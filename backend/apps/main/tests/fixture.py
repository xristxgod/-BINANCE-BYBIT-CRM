from typing import Type

import pytest

from rest_framework.test import APIClient

from .factories import AccountFactory
from .factories import TelegramFactory
from .factories import Google2FAFactory


@pytest.fixture
def api_client() -> Type[APIClient]:
    return APIClient


@pytest.fixture
def account_factory() -> Type[AccountFactory]:
    return AccountFactory


@pytest.fixture
def account_endpoint():
    from django.urls import reverse
    return reverse('')


@pytest.fixture
def telegram_factory() -> Type[TelegramFactory]:
    return TelegramFactory


@pytest.fixture
def telegram_endpoint():
    from django.urls import reverse
    return reverse('')


@pytest.fixture
def google2fa_factory() -> Type[Google2FAFactory]:
    return Google2FAFactory


@pytest.fixture
def google2fa_endpoint():
    from django.urls import reverse
    return reverse('')
