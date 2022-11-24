import faker
import factory.fuzzy
from factory.django import DjangoModelFactory

from ..models import Account
from ..models import Telegram
from ..models import Google2FA
from core.base import enums, factories


class AccountFactory(DjangoModelFactory):
    class Meta:
        model = Account

    name = factory.Sequence(lambda n: "title#%d" % n)
    network = factory.Iterator(enums.AccountNetwork)
    active = True
    user = factory.SubFactory(factories.UserFactory)

    class Params:
        inactive = factory.Trait(
            active=False
        )


class TelegramFactory(DjangoModelFactory):
    class Meta:
        model = Telegram

    chat_id = factory.LazyAttribute(lambda _: faker.Faker())
    active = True
    user = factory.SubFactory(factories.UserFactory)

    class Params:
        inactive = factory.Trait(
            active=False
        )


class Google2FAFactory(DjangoModelFactory):
    class Meta:
        model = Google2FA

    code = ''
    qr_code = ''
    active = True
    user = factory.SubFactory(factories.UserFactory)

    class Params:
        inactive = factory.Trait(
            active=False
        )
