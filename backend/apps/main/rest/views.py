from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from drf_spectacular.utils import extend_schema

from ..models import Account
from .serializers import AccountSerializer
# from core.login.authentication import ApiTokenAuthentication


class AccountsView(GenericAPIView):
    # authentication_classes = (ApiTokenAuthentication,)

    @extend_schema(
        request=None,
        responses={
            200: serializers.ListSerializer(
                child=AccountSerializer()
            )
        },
        summary='Accounts',
        description='Accounts'
    )
    def get(self, request, *args, **kwargs):

        accounts = Account.objects.all()

        return Response(AccountSerializer(
            accounts, many=True
        ))
