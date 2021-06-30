from core.serializers import ChoiceField
from apps.channels.serializers import ChannelSerializer
from rest_framework import serializers
from .models import IVSStream, Show
from django.conf import settings

class IVSStreamSerializer(serializers.ModelSerializer):
    cdn = serializers.ReadOnlyField(default=settings.AWS_IVS_VIDEO_CDN)
    recording_status = ChoiceField(choices=IVSStream.RECORDING_STATUS_CHOICES)
    class Meta:
        model = IVSStream
        fields = ('id', 'aws_stream_id', 'recording_duration', 'recording_status', 'show', 'channel', 's3_path', 's3_bucket', 'cdn')
        read_only_fields = ('aws_stream_id', 'recording_duration', 'recording_status', 'channel', 's3_path', 's3_bucket', 'cdn')

class ShowSerializer(serializers.ModelSerializer):
    channel = ChannelSerializer(read_only=True)
    stream = IVSStreamSerializer(read_only=True)
    class Meta:
        model = Show
        fields = ('id', 'name', 'description', 'channel', 'display_pic', 'products', 'time', 'stream')
        read_only_fields = ('channel',)
        depth = 1

class WriteShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = ('id', 'name', 'description', 'channel', 'display_pic', 'products', 'time', 'video')
        read_only_fields = ('channel',)
                