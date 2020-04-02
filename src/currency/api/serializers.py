from rest_framework import serializers

from currency.models import Rate
from account.models import Contact


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = (
            'id',
            'created',
            'get_currency_display',
            'currency',
            'buy',
            'sale',
            'get_source_display',
            'source',
        )
        extra_kwargs = {
            'currency': {'write_only': True},
            'source': {'write_only': True},
        }

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = (
            'id',
            'email',
            'title',
            'body',
            'created',
        )
        extra_kwargs = {
            'email': {'write_only': True},
            'title': {'write_only': True},
        }

