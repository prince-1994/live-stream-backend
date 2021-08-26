from apps.social.models import Social
from rest_framework import viewsets
from .serializers import SocialSerializer
from rest_framework.permissions import IsAuthenticated
from apps.channels.models import Channel
from rest_framework.exceptions import PermissionDenied


class SocialViewSet(viewsets.ModelViewSet):
    serializer_class = SocialSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        channel = Channel.objects.filter(owner=self.request.user).first()
        if not channel:
            raise PermissionDenied("Channel does not exist")
        return Social.objects.filter(channel=channel)
