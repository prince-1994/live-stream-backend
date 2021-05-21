from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from .models import Show
from .serializers import ShowSerializer, EditShowSerializer
from .permissions import *

class EditShowViewSet(viewsets.ModelViewSet):
    serializer_class = EditShowSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsShowOwner)

    def get_queryset(self):
        channel_id = self.kwargs['channel_id']
        return Show.objects.filter(channel__id = channel_id)

class ShowViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ShowSerializer
    permission_classes = (AllowAny,)
    queryset = Show.objects.all()
