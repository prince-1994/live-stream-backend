from apps.products.serializers import CategorySerializer
from apps.channels.models import Channel
from apps.products.models import Product
from rest_framework import serializers
from apps.checkout.models import CartItem

class EditCartProductChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ('id', 'name')

class EditCartProductSerializer(serializers.ModelSerializer):
    channel = EditCartProductChannelSerializer(read_only=True)
    category = CategorySerializer()
    class Meta:
        model = Product
        fields = ('id', 'name', 'primary_image', 'channel', 'category', 'price')

class EditCartSerializer(serializers.ModelSerializer):
    product=EditCartProductSerializer(read_only=True)
    class Meta:
        model = CartItem
        fields = ('id', 'product', 'quantity')
        depth = 1
