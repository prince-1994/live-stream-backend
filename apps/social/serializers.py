from apps.social.models import Social
from .serializers import Social
from rest_framework import serializers
from core.serializers import ChoiceField
from rest_framework.exceptions import PermissionDenied
from apps.channels.models import Channel


class SocialSerializer(serializers.ModelSerializer):
    type = ChoiceField(choices=Social.SOCIAL_ACCOUNT_TYPES)

    class Meta:
        model = Social
        fields = ("id", "name", "rtmp_ingest", "rtmp_key", "type")

    def create(self, validated_data):
        user = self.context["request"].user
        channel = Channel.objects.filter(owner=user).first()
        if not channel:
            raise PermissionDenied("channel does not exist")
        print(channel)
        obj = Social.objects.create(channel=channel, **validated_data)
        obj.save()
        return obj
