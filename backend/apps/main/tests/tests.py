import pytest


@pytest.mark.django_db
class TestAccount:
    def test_account_serializer(
            self,
            api_client,
            account_endpoint,
            account_factory,
    ):
        from ..rest.serializers import AccountSerializer
        pass

    def test_account_endpoint(
            self,
            api_client,
            account_endpoint,
            account_factory
    ):
        pass
