from apps.products.serializers import ProductSerializer
from apps.images.specs import Image1600x900, Image320x180
from apps.images.serializers import ImageSpecField
from apps.products.models import Product
from rest_framework.exceptions import PermissionDenied
from core.serializers import ChoiceField
from apps.channels.serializers import ChannelSerializer
from rest_framework import serializers
from .models import IVSStream, Show
from django.conf import settings
from apps.channels.models import Channel
from django.http.response import Http404
from datetime import timedelta, datetime
from apps.shows.constants import *
from django.utils.timezone import utc


class IVSStreamSerializer(serializers.ModelSerializer):
    cdn = serializers.ReadOnlyField(default=settings.AWS_IVS_VIDEO_CDN)
    recording_status = ChoiceField(choices=IVSStream.RECORDING_STATUS_CHOICES)

    class Meta:
        model = IVSStream
        fields = (
            "id",
            "aws_stream_id",
            "recording_duration",
            "recording_status",
            "show",
            "channel",
            "s3_path",
            "s3_bucket",
            "cdn",
            "is_live",
        )
        read_only_fields = (
            "aws_stream_id",
            "recording_duration",
            "recording_status",
            "channel",
            "s3_path",
            "s3_bucket",
            "cdn",
            "is_live",
        )


class ShowSerializer(serializers.ModelSerializer):
    channel = ChannelSerializer(read_only=True)
    stream = IVSStreamSerializer(read_only=True)
    display_pic = ImageSpecField(
        specs={
            "image_1600x900": Image1600x900,
            "image_320x180": Image320x180,
        },
        base=True,
    )
    products = ProductSerializer(read_only=True, many=True)

    class Meta:
        model = Show
        fields = (
            "id",
            "name",
            "description",
            "channel",
            "display_pic",
            "products",
            "time",
            "stream",
        )
        read_only_fields = (
            "channel",
            "display_pic",
        )
        depth = 1


class WriteShowSerializer(serializers.ModelSerializer):
    display_pic = ImageSpecField(
        specs={
            "image_1600x900": Image1600x900,
            "image_320x180": Image320x180,
        },
        base=True,
    )

    class Meta:
        model = Show
        fields = (
            "id",
            "name",
            "description",
            "channel",
            "products",
            "time",
            "display_pic",
        )
        read_only_fields = ("channel",)

    def create(self, validated_data):
        user = self.context["request"].user
        channel = Channel.objects.filter(owner=user).first()
        if not channel:
            raise PermissionDenied("channel does not exist")
        time = validated_data.get("time")
        time_delta = timedelta(minutes=SHOW_TIME_DELTA)
        last_show = channel.shows.filter(
            time__gte=time - time_delta,
            time__lte=time + time_delta,
        ).first()
        now = datetime.utcnow().replace(tzinfo=utc)
        if last_show or time - now < timedelta(minutes=0):
            print(time, now, last_show)
            raise PermissionDenied("Time clashes with another show.")
        product_ids = set(
            product.id for product in Product.objects.filter(channel=channel)
        )
        add_products = validated_data.pop("products")
        for product in add_products:
            if product.id not in product_ids:
                raise Http404("Product not found")
        display_pic = validated_data.pop("display_pic", None)
        obj = Show.objects.create(channel=channel, **validated_data)
        obj.display_pic = display_pic
        obj.save()
        for product in add_products:
            obj.products.add(product)
        return obj

    def update(self, instance, validated_data):
        stream = IVSStream.objects.filter(show=instance).first()
        if stream:
            raise PermissionDenied("This show is already live or has completed.")
        user = self.context["request"].user
        channel = Channel.objects.filter(owner=user).first()
        if not channel:
            raise PermissionDenied("channel does not exist")
        time = validated_data.get("time")
        time_delta = timedelta(minutes=SHOW_TIME_DELTA)
        last_shows = channel.shows.filter(
            time__gte=time - time_delta,
            time__lte=time + time_delta,
        )[:2]
        now = datetime.utcnow().replace(tzinfo=utc)
        if (
            len(last_shows) >= 2
            or (len(last_shows) == 1 and last_shows[0].id != instance.id)
            or time - now < timedelta(minutes=0)
        ):
            print(last_shows, time, now, time_delta)
            raise PermissionDenied("Time clashes with another show.")

        return super().update(instance, validated_data)
