from rest_framework.response import Response
from rest_framework import viewsets,status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Channel
from .serializers import ChannelSerializer, EditChannelSerializer
from .permissions import *
import boto3

class EditChannelViewSet(viewsets.ModelViewSet):
    serializer_class = EditChannelSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsChannelOwner)

    def get_queryset(self):
        owner = self.request.user.id
        return Channel.objects.filter(owner__id = owner)

class ChannelViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ChannelSerializer
    permission_classes = (AllowAny,)
    queryset = Channel.objects.all()

@api_view()
@permission_classes([AllowAny,])
def get_AWS_Channel(request, channel_id):
    channel = Channel.objects.get(pk=channel_id)
    ivs_client = boto3.client('ivs', region_name='us-west-2')
    response = ivs_client.get_channel(arn=channel.arn)
    return Response(response.get('channel'))

@api_view()
@permission_classes([IsAuthenticated])
def get_AWS_Stream_Key(request, channel_id):
    channel = request.user.channels.all()[0]
    if channel.id != channel_id:
        return Response({ 
            "data" : { 
                "error" : "You do not have permissions"
            }
        },
        status=status.HTTP_401_UNAUTHORIZED)
    ivs_client = boto3.client('ivs', region_name='us-west-2')
    response = ivs_client.get_stream_key(arn=channel.stream_key_arn)
    return Response(response.get('streamKey'))