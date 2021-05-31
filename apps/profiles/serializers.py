from apps.profiles.models import Address
from rest_framework import serializers

class EditAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'type', 'name', 'line1', 'line2', 'landmark', 'city', 'state', 'country', 'postal_code', 'phone_no')

    # Use this method for the custom field
    def _user(self):
        request = self.context.get('request', None)
        if request:
            return request.user
        return None

    def create(self, validated_data):
        user = self._user()
        address = Address.objects.create(user=user, **validated_data)
        address.save()
        return address
