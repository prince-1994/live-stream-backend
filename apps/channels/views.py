from re import search
from rest_framework.response import Response
from rest_framework import viewsets,status, filters
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
        print(self.request.user)
        owner = self.request.user.id
        return Channel.objects.filter(owner__id = owner)

class ChannelViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ChannelSerializer
    permission_classes = (AllowAny,)
    queryset = Channel.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

@api_view()
@permission_classes([AllowAny,])
def get_aws_channel(request, channel_id):
    channel = Channel.objects.get(pk=channel_id)
    ivs_client = boto3.client('ivs', region_name='us-west-2')
    response = ivs_client.get_channel(arn=channel.arn)
    return Response(response.get('channel'))

@api_view()
@permission_classes([AllowAny,])
def get_aws_stream(request, channel_id):
    channel = Channel.objects.get(pk=channel_id)
    ivs_client = boto3.client('ivs', region_name='us-west-2')
    try:
        response = ivs_client.get_stream(channelArn=channel.arn)
        return Response(response.get('stream'))
    except:
        return Response({'stream' : 'No live stream is present'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view()
@permission_classes([IsAuthenticated])
def get_aws_stream_key(request, channel_id):
    channel = Channel.objects.get(pk=channel_id)
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
    