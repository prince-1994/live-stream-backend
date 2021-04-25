from rest_framework import serializers
from .models import Channel, Video
import mux_python
import os

configuration = mux_python.Configuration()
configuration.username = os.environ['MUX_TOKEN_ID']
configuration.password = os.environ['MUX_TOKEN_SECRET']

live_api = mux_python.LiveStreamsApi(mux_python.ApiClient(configuration))
new_asset_settings = mux_python.CreateAssetRequest(playback_policy=[mux_python.PlaybackPolicy.PUBLIC])


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ('id', 'name', 'description', 'owner', 'display_pic', 'background_pic')
        read_only_fields = ('owner',)

    # Use this method for the custom field
    def _user(self):
        request = self.context.get('request', None)
        if request:
            return request.user
        return None

    def create(self, validated_data):
        user = self._user()
        # create_live_stream_request = mux_python.CreateLiveStreamRequest(playback_policy=[mux_python.PlaybackPolicy.PUBLIC], new_asset_settings=new_asset_settings)
        # create_live_stream_response = live_api.create_live_stream(create_live_stream_request)
        # stream_key = create_live_stream_response.data.stream_key
        obj = Channel.objects.create(owner=user,**validated_data)
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