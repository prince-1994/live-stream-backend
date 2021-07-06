from apps.images.specs import Image128x128, Image256x256, Image512x512, Image64x64
from apps.images.serializers import ImageSpecField
from apps.channels.models import Channel
from rest_framework import serializers
from .models import Category, Product, ProductImage
from taggit_serializer.serializers import (TaggitSerializer, TagListSerializerField)
from rest_framework.exceptions import PermissionDenied

class ProductImageSerializer(serializers.ModelSerializer):
    image = ImageSpecField(specs={
        'image_64x64' : Image64x64,
        'image_128x128' : Image128x128,
        'image_256x256' : Image256x256,
        'image_512x512' : Image512x512,
    }, base=True)
    class Meta:
        model = ProductImage
        fields = ('id', 'default', 'image')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

class ProductSerializer(TaggitSerializer, serializers.ModelSerializer) :
    tags = TagListSerializerField()
    images = ProductImageSerializer(many=True)
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'channel', 'price', 'category', 'selling_price', 'tags', 'images')
        read_only_fields = ('channel',)

    def create(self, validated_data):
        user = self.context['request'].user
        channel = Channel.objects.filter(owner=user).first()
        if not channel:
            raise PermissionDenied("channel does not exist")
        product_images_data = validated_data.pop('images', [])
        product = Product.objects.create(channel=channel, **validated_data)
        product.save()
        for product_image_data in product_images_data:
            image = product_image_data.pop('image', None)
            product_image = ProductImage.objects.create(product=product, **product_image_data)
            product.image = image
            product_image.save()
        return product

    def update(self, instance, validated_data):
        request = self.context['request']
        user = request.user
        query_params_dict = dict(request.query_params)
        delete_image_ids = query_params_dict.get('delete_images')
        if delete_image_ids:
            for delete_image_id in delete_image_ids:
                try:
                    id = int(delete_image_id)
                    image = ProductImage.objects.filter(pk=id).first()
                    if image and image.product.channel.owner == user:
                        image.delete()
                except ValueError as e:
                    print(e)
        if ('images' in validated_data):
            images_data = validated_data.pop('images')
            for image_data in images_data:
                image = ProductImage.objects.create(product=instance, **image_data)
                image.save()
        try:
            default_id = int(request.query_params.get('default_image'))
            print(default_id)
        except Exception:
            default_id = None
        if default_id:
            for image in ProductImage.objects.filter(product=instance):
                if image.default and image.id != default_id:
                    image.default = False
                    image.save()
                elif (not image.default) and image.id == default_id:
                    image.default = True
                    image.save()
        return instance