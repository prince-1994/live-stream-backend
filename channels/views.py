from rest_framework import viewsets
from .models import Video, Channel
from .serializers import ChannelSerializer, VideoSerializer
from .permissions import *
from tslclone.permissions import IsAuthenticatedAndOwner

class ChannelViewSet(viewsets.ModelViewSet):
    serializer_class = ChannelSerializer
    permission_classes = (IsAuthenticatedAndOwner,)

    def get_queryset(self):
        owner = self.request.query_params.get('user')
        if owner is not None:
            return Channel.objects.filter(owner__id = owner)
        return Channel.objects.all()
        

class VideoViewSet(viewsets.ModelViewSet):
    serializer_class = VideoSerializer
    permission_classes = (VideoPermission,)

    def get_queryset(self):
        channel = self.request.query_params.get('channel')
        if channel is not None:
            return Video.objects.filter(channel__id = channel)
        return Video.objects.all()
        