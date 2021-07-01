from apps.profiles.models import Address
from rest_framework import serializers

class EditAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'type', 'name', 'line1', 'line2', 'landmark', 'city', 'state', 'country', 'postal_code', 'phone_no')