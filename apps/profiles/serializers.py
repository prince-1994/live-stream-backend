from core.serializers import ChoiceField
from apps.profiles.models import Address
from rest_framework import serializers

class AddressSerializer(serializers.ModelSerializer):
    country = ChoiceField(choices=Address.COUNTRY_CHOICES)
    type = ChoiceField(choices=Address.TYPE_CHOICES)
    class Meta:
        model = Address
        fields = ('id', 'type', 'name', 'line1', 'line2', 'landmark', 'city', 'state', 'country', 'postal_code', 'phone_no')