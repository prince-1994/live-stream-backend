from botocore import model
from rest_framework import serializers
from .models import Channel
import boto3
from django.conf import settings

class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ('id', 'name', 'description', 'owner', 'display_pic', 'background_pic', 'arn',)
        read_only_fields = ('owner', 'arn', 'stream_key_arn')

class EditChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ('id', 'name', 'description', 'owner', 'display_pic', 'background_pic', 'arn', 'stream_key_arn')
        read_only_fields = ('owner', 'arn', 'stream_key_arn')

    # Use this method for the custom field
    def _user(self):
        request = self.context.get('request', None)
        if request:
            return request.user
        return None

    def create(self, validated_data):
        user = self._user()
        ivs_client = boto3.client('ivs', region_name='us-west-2')
        alphanumeric = [character for character in validated_data.get('name') if character.isalnum()]
        alphanumeric = "".join(alphanumeric)
        response = ivs_client.create_channel(
            name=alphanumeric, 
            latencyMode='LOW',
            type=settings.AWS_S3_CHANNEL_TYPE,
            recordingConfigurationArn=settings.AWS_S3_RECORDING_CONFIGURATION_ARN,
            tags={
                'env' : settings.ENV
            }
        )
        obj = Channel.objects.create(
            owner=user,
            arn=response.get('channel').get('arn'),
            stream_key_arn=response.get('streamKey').get('arn'),
            **validated_data)
        obj.save()
        return obj


