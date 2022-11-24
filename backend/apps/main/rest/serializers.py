from rest_framework import serializers

from ..models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            'name', 'network', 'active', 'user'
        )
        read_only_fields = fields
