from apps.channels.models import Channel
from rest_framework import serializers
from .models import Category, Product
from taggit_serializer.serializers import (TaggitSerializer, TagListSerializerField)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

class ProductSerializer(TaggitSerializer, serializers.ModelSerializer) :
    tags = TagListSerializerField()
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'channel', 'price', 'primary_image', 'category', 'selling_price', 'tags')
        read_only_fields = ('channel',)