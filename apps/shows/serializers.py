from rest_framework.fields import ChoiceField
from apps.channels.serializers import ChannelSerializer
from django.http.response import Http404
from apps.products.models import Product
from rest_framework import serializers
from .models import IVSVideo, Show
from apps.channels.models import Channel
from django.conf import settings

class IVSVideoSerializer(serializers.ModelSerializer):
    cdn = serializers.ReadOnlyField(default=settings.AWS_IVS_VIDEO_CDN)
    recording_status = ChoiceField(choices=IVSVideo.RECORDING_STATUS_CHOICES)
    class Meta:
        model = IVSVideo
        fields = ('id', 'aws_stream', 'recording_duration', 'recording_status', 'show', 'channel', 's3_path', 's3_bucket', 'cdn')
        read_only_fields = ('aws_stream', 'recording_duration', 'recording_status', 'channel', 's3_path', 's3_bucket', 'cdn')

class ShowSerializer(serializers.ModelSerializer):
    channel = ChannelSerializer(read_only=True)
    video = IVSVideoSerializer(read_only=True)
    class Meta:
        model = Show
        fields = ('id', 'name', 'description', 'channel', 'display_pic', 'products', 'time', 'video')
        read_only_fields = ('channel',)
        depth = 1

class WriteShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = ('id', 'name', 'description', 'channel', 'display_pic', 'products', 'time', 'video')
        read_only_fields = ('channel',)
                