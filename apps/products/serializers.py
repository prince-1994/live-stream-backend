from apps.images.specs import Image128x128, Image256x256, Image512x512, Image64x64
from apps.images.serializers import ImageSerializer, ImageSpecField
from apps.images.models import ImageAlbum
from django.db.models.expressions import Value
from apps.channels.models import Channel
from rest_framework import serializers
from .models import Category, Product
from taggit_serializer.serializers import (TaggitSerializer, TagListSerializerField)
from rest_framework.exceptions import PermissionDenied
from drf_extra_fields.fields import Base64ImageField

class ProductImageSerializer(ImageSerializer):
    base = ImageSpecField(specs={
        'image_64x64' : Image64x64,
        'image_128x128' : Image128x128,
        'image_256x256' : Image256x256,
        'image_512x512' : Image512x512,
    }, base=True)

class ProductImageAlbumSerializer(ImageAlbum):
    images = ProductImageSerializer(many=True, read_only=True)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

class ProductSerializer(TaggitSerializer, serializers.ModelSerializer) :
    tags = TagListSerializerField()
    image_album = ProductImageAlbumSerializer()
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'channel', 'price', 'category', 'selling_price', 'tags', 'image_album')
        read_only_fields = ('channel',)

    def create(self, validated_data):
        user = self.context['request'].user
        channel = Channel.objects.filter(owner=user).first()
        if not channel:
            raise PermissionDenied("channel does not exist")
        product = Product.objects.create(channel=channel, **validated_data)
        image_album = ImageAlbum.objects.create(path=f"products/{product.id}/images/")
        product.image_album = image_album
        product.save()
        product.save()
        return product