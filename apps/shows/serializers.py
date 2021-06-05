from apps.channels.serializers import ChannelSerializer
from django.http.response import Http404
from apps.products.models import Product
from rest_framework import serializers
from .models import IVSVideo, Show
from apps.channels.models import Channel

class EditShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = ('id', 'name', 'description', 'channel', 'display_pic', 'products', 'time')
        read_only_fields = ('channel',)

    def create(self, validated_data):
        channel_id = self.context.get('request').parser_context.get('kwargs').get('channel_id')
        channel = Channel.objects.filter(id=channel_id).first()
        product_ids = set(product.id for product in Product.objects.filter(channel__id=channel_id))
        add_products = validated_data.pop('products')
        for product in add_products:
            if product.id not in product_ids:
                raise Http404("Product not found")
        print("show creation start")
        obj = Show.objects.create(channel=channel,**validated_data)
        obj.save()
        for product in add_products:
            obj.products.add(product)
        return obj

class ShowSerializer(serializers.ModelSerializer):
    channel = ChannelSerializer(read_only=True)

    class Meta:
        model = Show
        fields = ('id', 'name', 'description', 'channel', 'display_pic', 'products', 'time')
        read_only_fields = ('name', 'description', 'channel', 'display_pic', 'products', 'time')
        depth = 1

class IVSVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = IVSVideo
        fields = ('id', 'aws_stream_id', 'recording_duration', 'recording_status', 'show', 'channel', 's3_path', 's3_bucket')