from apps.products.serializers import ProductSerializer
from apps.images.specs import Image1600x900, Image320x180
from apps.images.serializers import ImageAlbumSerializer, ImageSerializer, ImageSpecField
from apps.images.models import ImageAlbum
from apps.products.models import Product
from rest_framework.exceptions import PermissionDenied
from core.serializers import ChoiceField
from apps.channels.serializers import ChannelSerializer
from rest_framework import serializers
from .models import IVSStream, Show
from django.conf import settings
from apps.channels.models import Channel
from django.http.response import Http404

class ShowDisplayPicImageSerializer(ImageSerializer):
    base = ImageSpecField(specs={
        'image_1600x900' : Image1600x900,
        'image_320x180' : Image320x180,
    }, base=True)

class ShowDisplayPicAlbumSerializer(ImageAlbumSerializer):
    images = ShowDisplayPicImageSerializer(many=True, read_only=True)

class IVSStreamSerializer(serializers.ModelSerializer):
    cdn = serializers.ReadOnlyField(default=settings.AWS_IVS_VIDEO_CDN)
    recording_status = ChoiceField(choices=IVSStream.RECORDING_STATUS_CHOICES)
    class Meta:
        model = IVSStream
        fields = ('id', 'aws_stream_id', 'recording_duration', 'recording_status', 'show', 'channel', 's3_path', 's3_bucket', 'cdn', 'is_live')
        read_only_fields = ('aws_stream_id', 'recording_duration', 'recording_status', 'channel', 's3_path', 's3_bucket', 'cdn', 'is_live')


class ShowSerializer(serializers.ModelSerializer):
    channel = ChannelSerializer(read_only=True)
    stream = IVSStreamSerializer(read_only=True)
    display_pic_album = ShowDisplayPicAlbumSerializer()
    products = ProductSerializer(read_only=True, many=True)
    class Meta:
        model = Show
        fields = ('id', 'name', 'description', 'channel', 'display_pic_album', 'products', 'time', 'stream')
        read_only_fields = ('channel', 'display_pic_album',)
        depth = 1

class WriteShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = ('id', 'name', 'description', 'channel', 'products', 'time')
        read_only_fields = ('channel',)

    def create(self, validated_data):
        user = self.context['request'].user
        channel = Channel.objects.filter(owner=user).first()
        if not channel:
            raise PermissionDenied("channel does not exist")
        product_ids = set(
            product.id for product in Product.objects.filter(channel=channel)
        )
        add_products = validated_data.pop("products")
        for product in add_products:
            if product.id not in product_ids:
                raise Http404("Product not found")
        print(channel, "-----------------", validated_data)
        obj = Show.objects.create(channel=channel, **validated_data)
        image_album = ImageAlbum.objects.create(owner=user, path=f"shows/{obj.id}/images/")
        obj.display_pic_album = image_album
        obj.save()
        for product in add_products:
            obj.products.add(product)
        return obj
                