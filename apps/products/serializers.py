from apps.channels.models import Channel
from rest_framework import serializers
from .models import Category, Product
from taggit_serializer.serializers import (TaggitSerializer, TagListSerializerField)

class EditProductSerializer(TaggitSerializer,serializers.ModelSerializer):
    # images = ProductImageSerializer(many=True)
    tags = TagListSerializerField()
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'channel', 'price', 'primary_image', 'sku_id', 'category', 'selling_price', 'tags')
        read_only_fields = ('channel',)

    def _user(self):
        request = self.context.get('request', None)
        if request:
            return request.user
        return None

    def create(self, validated_data):
        channel_id = self.context.get('request').parser_context.get('kwargs').get(
            'channel_id')
        
        channel = Channel.objects.filter(id=channel_id).first()
        obj = Product.objects.create(channel=channel,**validated_data)
        obj.save()
        return obj

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name');

class ProductSerializer(TaggitSerializer, serializers.ModelSerializer) :
    category = serializers.StringRelatedField()
    tags = TagListSerializerField()
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'channel', 'price', 'primary_image', 'category', 'selling_price', 'tags')
        read_only_fields = ('id', 'name', 'description', 'channel', 'price', 'primary_image', 'category', 'selling_price', 'tags')