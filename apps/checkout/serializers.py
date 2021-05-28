from apps.products.serializers import CategorySerializer
from apps.channels.models import Channel
from apps.products.models import Product
from rest_framework import serializers
from apps.checkout.models import CartItem

class CartProductChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ('id', 'name')

class CartProductSerializer(serializers.ModelSerializer):
    channel = CartProductChannelSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Product
        fields = ('id', 'name', 'primary_image', 'channel', 'category', 'price')

class CartSerializer(serializers.ModelSerializer):
    product=CartProductSerializer(read_only=True)
    class Meta:
        model = CartItem
        fields = ('id', 'product', 'quantity')
        depth = 1


class EditCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('id', 'product', 'quantity')
