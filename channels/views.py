from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from .models import Channel
from .serializers import ChannelSerializer
from .permissions import *

class EditChannelViewSet(viewsets.ModelViewSet):
    serializer_class = ChannelSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsChannelOwner)

    def get_queryset(self):
        owner = self.request.user.id
        return Channel.objects.filter(owner__id = owner)

class ChannelViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ChannelSerializer
    permission_classes = (AllowAny,)
    queryset = Channel.objects.all()
