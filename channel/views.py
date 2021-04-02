from rest_framework import viewsets
from .models import *
from .serializers import *
from .permissions import *

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (UserProfilePermission,)

class ChannelViewSet(viewsets.ModelViewSet):
    serializer_class = ChannelSerializer
    permission_classes = (ChannelPermission,)

    def get_queryset(self):
        user = self.request.query_params.get('user')
        if user is not None:
            return Channel.objects.filter(user__id = user)
        return Channel.objects.all()

class VideoViewSet(viewsets.ModelViewSet):
    serializer_class = VideoSerializer
    permission_classes = (VideoPermission,)

    def get_queryset(self):
        channel = self.request.query_params.get('channel')
        if channel is not None:
            return Video.objects.filter(channel__id = channel)
        return Video.objects.all()

    # def create(self, request, *args, **kwargs):
        