from apps.profiles.models import Address
from django.db import models
from django.db.models import fields
from rest_framework.decorators import action
from rest_framework.fields import ReadOnlyField
from apps.products.serializers import CategorySerializer
from apps.channels.models import Channel
from apps.products.models import Product
from rest_framework import serializers
from apps.checkout.models import CartItem, Order, OrderItem, OrderItemStatus
from apps.profiles.serializers import EditAddressSerializer
from tslclone.serializers import ChoiceField


# cart related serializers
class CartProductChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ('id', 'name')

class CartProductSerializer(serializers.ModelSerializer):
    channel = CartProductChannelSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Product
        fields = ('id', 'name', 'primary_image', 'channel', 'category', 'price', 'selling_price')

class CartSerializer(serializers.ModelSerializer):
    product=CartProductSerializer(read_only=True)
    class Meta:
        model = CartItem
        fields = ('id', 'product', 'quantity')
        depth = 1


class WriteCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('id', 'product', 'quantity')


# order related serializer
class OrderItemStatusSerializer(serializers.ModelSerializer):
    value = ChoiceField(choices=OrderItemStatus.STATUS_CHOICES)
    class Meta:
        model = OrderItemStatus
        fields = ('id', 'order_item', 'date', 'value', 'created_at', 'updated_at')
        read_only_fields = ('order_item', 'date', 'value', 'created_at', 'updated_at')

class OrderItemSerializer(serializers.ModelSerializer):
    product=CartProductSerializer(read_only=True)
    address=EditAddressSerializer(read_only=True)
    status = ChoiceField(choices=OrderItem.STATUS_CHOICES)
    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'order', 'price', 'total_amount', 'selling_price', 'quantity', 'address', 'status')
        read_only_fields = ('product', 'price', 'order', 'total_amount', 'selling_price', 'quantity', 'address')

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(read_only=True, many=True)
    payment_status = ChoiceField(choices=Order.PAYMENT_STATUS_CHOICES)
    class Meta:
        model = Order
        fields = ('id', 'user', 'total_amount', 'payment_status', 'items', 'created_at')
        read_only_fields = ('user', 'total_amount', 'payment_status', 'items', 'created_at')

class CreateOrderItemSerializer(serializers.Serializer):
    product = serializers.IntegerField()
    quantity = serializers.IntegerField()
    address = serializers.IntegerField()
