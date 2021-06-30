from apps.channels.models import Channel
from rest_framework import serializers
from .models import Category, Product, ProductImage
from taggit_serializer.serializers import (TaggitSerializer, TagListSerializerField)
from rest_framework.exceptions import PermissionDenied
from drf_extra_fields.fields import Base64ImageField

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

class ProductImageSerializer(serializers.ModelSerializer):
    image_96x96 = serializers.ImageField(read_only=True)
    image_128x128 = serializers.ImageField(read_only=True)
    image_512x512 = serializers.ImageField(read_only=True)
    base = Base64ImageField()
    class Meta:
        model = ProductImage
        fields = ('id', 'base', 'image_96x96', 'image_128x128', 'image_512x512')
        extra_kwargs = {
            'base': {'write_only' : True}
        }

class ProductSerializer(TaggitSerializer, serializers.ModelSerializer) :
    tags = TagListSerializerField()
    images = ProductImageSerializer(many=True)
    primary_image = Base64ImageField()
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'channel', 'price', 'primary_image', 'category', 'selling_price', 'tags', 'images')
        read_only_fields = ('channel',)

    def create(self, validated_data):
        user = self.context['request'].user
        channel = Channel.objects.filter(owner=user).first()
        if not channel:
            raise PermissionDenied("channel does not exist")
        images_data = validated_data.pop('images')
        product = Product.objects.create(channel=channel, **validated_data)
        product.save()
        for image_data in images_data:
            image = ProductImage.objects.create(product=product, **image_data)
            image.save()
        return product



    def update(self, instance, validated_data):
        request = self.context['request']
        user = request.user
        channel = Channel.objects.filter(owner=user).first()
        if not channel:
            raise PermissionDenied("channel does not exist")
        delete_image_ids = dict(request.query_params).get('delete_images')
        if delete_image_ids:
            print(dict(request.query_params))
            for delete_image_id in delete_image_ids:
                try:
                    id = int(delete_image_id)
                    productImage = ProductImage.objects.filter(pk=id).first()
                    if productImage and productImage.product.channel == channel:
                        productImage.delete()
                        print(productImage)
                except ValueError as e:
                    print(e)
        if ('images' in validated_data):
            images_data = validated_data.pop('images')
            for image_data in images_data:
                image = ProductImage.objects.create(product=instance, **image_data)
                image.save()
        
        product = super(ProductSerializer, self).update(instance, validated_data)
        return product