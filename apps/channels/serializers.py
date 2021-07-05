from apps.images.specs import Image128x128, Image1500x400, Image256x256, Image36x36, Image48x48
from apps.images.serializers import ImageAlbumSerializer, ImageSerializer, ImageSpecField
from apps.images.models import Image, ImageAlbum
from rest_framework import serializers
from .models import Channel
import boto3
from django.conf import settings


class ChannelDisplayPicSerializer(ImageSerializer):
    base = ImageSpecField(specs={
        'image_36x36' : Image36x36,
        'image_48x48' : Image48x48,
        'image_128x128' : Image128x128,
        'image_256x256' : Image256x256
    }, base=True)

class ChannelDisplayPicAlbumSerializer(ImageAlbumSerializer):
    images = ChannelDisplayPicSerializer(many=True, read_only=True)

class ChannelBackgroundPicSerializer(ImageSerializer):
    base = ImageSpecField(specs={
        'image_1500x400' : Image1500x400,
    }, base=True)

class ChannelBackgroundPicAlbumSerializer(ImageAlbumSerializer):
    images = ChannelBackgroundPicSerializer(many=True, read_only=True)

class ChannelSerializer(serializers.ModelSerializer):
    display_pic_album = ChannelDisplayPicAlbumSerializer(read_only=True)
    background_pic_album = ChannelBackgroundPicAlbumSerializer(read_only=True)
    class Meta:
        model = Channel
        fields = ('id', 'name', 'description', 'owner', 'display_pic_album', 'background_pic_album', 'arn')
        read_only_fields = ('owner', 'arn', 'display_pic_album', 'background_pic_album')