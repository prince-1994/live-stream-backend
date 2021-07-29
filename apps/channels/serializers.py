from apps.images.specs import (
    Image128x128,
    Image1500x400,
    Image256x256,
    Image36x36,
    Image48x48,
)
from apps.images.serializers import ImageSpecField
from rest_framework import serializers
from .models import Channel, background_pic_name
import boto3
from django.conf import settings
from apps.payout.models import Commission
from rest_framework.exceptions import PermissionDenied


class ChannelSerializer(serializers.ModelSerializer):
    display_pic = ImageSpecField(
        specs={
            "image_36x36": Image36x36,
            "image_48x48": Image48x48,
            "image_128x128": Image128x128,
            "image_256x256": Image256x256,
        },
        base=True,
    )
    background_pic = ImageSpecField(
        specs={
            "image_1500x400": Image1500x400,
        },
        base=True,
    )

    class Meta:
        model = Channel
        fields = (
            "id",
            "name",
            "description",
            "owner",
            "display_pic",
            "background_pic",
            "arn",
        )
        read_only_fields = ("owner", "arn")

    def create(self, validated_data):
        request = self.context["request"]
        user = request.user
        if not user.seller_activated:
            raise PermissionDenied("You do not have permissions to create channel")
        channel_count = Channel.objects.filter(owner=user).count()
        if channel_count > 0:
            raise PermissionDenied("Channel already exists")
        ivs_client = boto3.client(
            "ivs",
            region_name="us-west-2",
            aws_access_key_id=settings.AWS_IVS_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_IVS_SECRET_KEY,
        )
        alphanumeric = [
            character for character in validated_data.get("name") if character.isalnum()
        ]
        alphanumeric = "".join(alphanumeric)
        response = ivs_client.create_channel(
            name=alphanumeric,
            latencyMode="LOW",
            type=settings.AWS_IVS_CHANNEL_TYPE,
            recordingConfigurationArn=settings.AWS_IVS_RECORDING_CONFIGURATION_ARN,
            tags={"env": settings.ENV},
        )
        display_pic = validated_data.pop("display_pic", None)
        background_pic = validated_data.pop("background_pic", None)
        obj = Channel.objects.create(
            owner=user,
            arn=response.get("channel").get("arn"),
            stream_key_arn=response.get("streamKey").get("arn"),
            **validated_data
        )
        obj.display_pic = display_pic
        obj.background_pic = background_pic
        obj.save()
        commission = Commission.objects.create(channel=obj)
        commission.save()
        return obj
