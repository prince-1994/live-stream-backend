from apps.images.specs import Image128x128, Image1500x400, Image256x256, Image36x36, Image48x48
from apps.images.serializers import ImageSpecField
from rest_framework import serializers
from .models import Channel
import boto3
from django.conf import settings

class ChannelSerializer(serializers.ModelSerializer):
    display_pic = ImageSpecField(specs={
        'image_36x36' : Image36x36,
        'image_48x48' : Image48x48,
        'image_128x128' : Image128x128,
        'image_256x256' : Image256x256
    }, base=True)
    background_pic = ImageSpecField(specs={
        'image_1500x400' : Image1500x400,
    }, base=True)

    class Meta:
        model = Channel
        fields = ('id', 'name', 'description', 'owner', 'display_pic', 'background_pic', 'arn')
        read_only_fields = ('owner', 'arn')