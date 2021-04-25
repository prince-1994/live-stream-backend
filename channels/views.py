from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Video, Channel
from .serializers import ChannelSerializer, VideoSerializer
from .permissions import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from tslclone.permissions import IsAuthenticatedAndOwner

class ChannelViewSet(viewsets.ModelViewSet):
    serializer_class = ChannelSerializer
    permission_classes = (IsAuthenticatedAndOwner,)

    def get_queryset(self):
        owner = self.request.query_params.get('user_id')
        if owner is not None:
            return Channel.objects.filter(owner__id = owner)
        return Channel.objects.all()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_channel(request):
    owner = request.user
    channel = Channel.objects.filter(owner = owner).first()
    if channel is None:
        return Response({ "data" : "No channel was found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = ChannelSerializer(channel)
    print(serializer.data)
    return Response(serializer.data, status=status.HTTP_200_OK)



class VideoViewSet(viewsets.ModelViewSet):
    serializer_class = VideoSerializer
    permission_classes = (VideoPermission,)

    def get_queryset(self):
        channel = self.request.query_params.get('channel')
        if channel is not None:
            return Video.objects.filter(channel__id = channel)
        return Video.objects.all()
        