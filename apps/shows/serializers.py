from apps.products.models import Product
from drf_extra_fields.fields import Base64ImageField
from rest_framework.exceptions import PermissionDenied
from core.serializers import ChoiceField
from apps.channels.serializers import ChannelSerializer
from rest_framework import serializers
from .models import IVSStream, Show, ShowImage
from django.conf import settings
from apps.channels.models import Channel
from django.http.response import Http404

class IVSStreamSerializer(serializers.ModelSerializer):
    cdn = serializers.ReadOnlyField(default=settings.AWS_IVS_VIDEO_CDN)
    recording_status = ChoiceField(choices=IVSStream.RECORDING_STATUS_CHOICES)
    class Meta:
        model = IVSStream
        fields = ('id', 'aws_stream_id', 'recording_duration', 'recording_status', 'show', 'channel', 's3_path', 's3_bucket', 'cdn', 'is_live')
        read_only_fields = ('aws_stream_id', 'recording_duration', 'recording_status', 'channel', 's3_path', 's3_bucket', 'cdn', 'is_live')

class ShowImageSerilizer(serializers.ModelSerializer):
    base = Base64ImageField()
    image_720x1280 = serializers.ImageField()
    image_180x320 = serializers.ImageField()
    class Meta:
        model = ShowImage
        fields = ('id', 'base', 'image_720x1280', 'image_180x320')


class ShowSerializer(serializers.ModelSerializer):
    channel = ChannelSerializer(read_only=True)
    stream = IVSStreamSerializer(read_only=True)
    display_pic = ShowImageSerilizer(read_only=True)
    class Meta:
        model = Show
        fields = ('id', 'name', 'description', 'channel', 'display_pic', 'products', 'time', 'stream')
        read_only_fields = ('channel',)
        depth = 1

class WriteShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = ('id', 'name', 'description', 'channel', 'display_pic', 'products', 'time', 'stream')
        read_only_fields = ('channel',)

    def create(self, validated_data):
        user = self.request.user
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
        obj = Show.objects.save(channel=channel, **validated_data)
        for product in add_products:
            obj.products.add(product)
        return super().create(validated_data)
                