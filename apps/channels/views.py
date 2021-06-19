from os import stat
from re import search
from rest_framework.response import Response
from rest_framework import viewsets,status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.serializers import Serializer
from .models import Channel
from .serializers import ChannelSerializer, EditChannelSerializer
from .permissions import *
import boto3
from django.conf import settings

class EditChannelViewSet(viewsets.ModelViewSet):
    serializer_class = EditChannelSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsChannelOwner)

    def get_queryset(self):
        print(self.request.user)
        owner = self.request.user.id
        return Channel.objects.filter(owner__id = owner)

class ChannelViewSet(viewsets.ModelViewSet):
    serializer_class = ChannelSerializer
    permission_classes = (IsChannelOwner,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

    def get_queryset(self):
        is_channel_view = self.request.query_params.get('view') == 'channel'
        if is_channel_view and self.request.user.is_authenticated:
            return Channel.objects.filter(owner=self.request.user)
        return Channel.objects.all()

    def create(self, request, *args, **kwargs):
        user = self.request.user
        channel_count = Channel.objects.filter(owner=self.request.user).count()
        if channel_count > 0:
            return Response({"error" : "channel is already present"}, status.HTTP_403_FORBIDDEN) 
        ivs_client = boto3.client('ivs', region_name='us-west-2')
        serializer = ChannelSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        alphanumeric = [character for character in serializer.validated_data.get('name') if character.isalnum()]
        alphanumeric = "".join(alphanumeric)
        response = ivs_client.create_channel(
            name=alphanumeric, 
            latencyMode='LOW',
            type=settings.AWS_S3_CHANNEL_TYPE,
            recordingConfigurationArn=settings.AWS_S3_RECORDING_CONFIGURATION_ARN,
            tags={
                'env' : settings.ENV
            }
        )
        obj = Channel.objects.create(
            owner=user,
            arn=response.get('channel').get('arn'),
            stream_key_arn=response.get('streamKey').get('arn'),
            **serializer.validated_data)
        obj.save()
        serializer = ChannelSerializer(obj)
        return Response(serializer.data)
        
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
    