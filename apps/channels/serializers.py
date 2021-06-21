from botocore import model
from rest_framework import serializers
from .models import Channel
import boto3
from django.conf import settings

class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ('id', 'name', 'description', 'owner', 'display_pic', 'background_pic')
        read_only_fields = ('owner',)
