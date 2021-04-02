from django.db import models
from django.db.models import fields
from django.http import request
from rest_framework import serializers
from .models import Channel, UserProfile, Video
import uuid

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id','first_name', 'last_name', 'user')
        read_only_field = ('user')

class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ('id', 'name', 'description', 'stream', 'user', 'display_pic', 'background_pic')
        read_only_fields = ('user', 'stream')

    # Use this method for the custom field
    def _user(self):
        request = self.context.get('request', None)
        if request:
            return request.user
        return None

    def create(self, validated_data):
        user = self._user()
        stream = "stream-" + str(uuid.uuid4())
        obj = Channel.objects.create(user=user,stream=stream,**validated_data)
        obj.save()
        return obj

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('id', 'name', 'file', 'thumbnail', 'channel')
        read_only_fields = ('channel',)

    def create(self, validated_data):
        request = self.context.get('request')
        channel_id = request.data['channel']
        channel = Channel.objects.get(pk = channel_id)
        video = Video.objects.create(channel = channel, **validated_data)
        video.save()
        return video