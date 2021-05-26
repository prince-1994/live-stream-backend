from rest_framework import serializers
from apps.checkout.models import CartItem


class EditCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('id', 'product', 'quantity')
        depth = 1
