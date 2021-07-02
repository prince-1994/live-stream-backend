from django.http.response import Http404
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import viewsets,status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Channel
from .serializers import ChannelSerializer
from .permissions import *
import boto3
from django.conf import settings
from apps.payout.models import Commission
from tslclone.permissions import ReadOnly
from apps.channels.permissions import ChannelEditPermission
from rest_framework.decorators import action

class ChannelViewSet(viewsets.ModelViewSet):
    serializer_class = ChannelSerializer
    permission_classes = (ReadOnly|ChannelEditPermission,)
    search_fields = ['name', 'description']
    filterset_fields= ['owner']
    queryset = Channel.objects.all()

    def perform_create(self, serializer):
        if not self.request.user.seller_activated:
            raise PermissionDenied("You do not have permissions to create channel")
        channel_count = Channel.objects.filter(owner=self.request.user).count()
        if channel_count > 0:
            raise PermissionDenied("Channel already exists")
        user = self.request.user
        ivs_client = boto3.client('ivs', region_name='us-west-2')
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
        obj = serializer.save(
            owner=user,
            arn=response.get('channel').get('arn'),
            stream_key_arn=response.get('streamKey').get('arn'))
        commission = Commission.objects.create(channel=obj)
        commission.save()
        return super().perform_create(serializer)
    
    def perform_destroy(self, instance):
        ivs_client = boto3.client('ivs', region_name='us-west-2')
        ivs_client.delete_channel(arn=instance.arn)
        return super().perform_destroy(instance)

    @action(detail=False, methods=['get'], permission_classes=(), url_path='detail')
    def get_aws_channel(self, request):
        channel = Channel.objects.filter(owner=request.user).first()
        if not channel:
            raise Http404
        ivs_client = boto3.client('ivs', region_name='us-west-2')
        response = ivs_client.get_channel(arn=channel.arn)
        return Response(response.get('channel'))

    @action(detail=False, methods=['get'], permission_classes=(), url_path='stream-detail')
    def get_aws_stream(self, request):
        channel = Channel.objects.filter(owner=request.user).first()
        if not channel:
            raise Http404
        ivs_client = boto3.client('ivs', region_name='us-west-2')
        try:
            response = ivs_client.get_stream(channelArn=channel.arn)
            return Response(response.get('stream'))
        except:
            return Response({'stream' : 'No live stream is present'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['get'], permission_classes=(IsAuthenticated,), url_path='stream-key')
    def get_aws_stream_key(self, request):
        channel = Channel.objects.filter(owner=request.user).first()
        if not channel:
            raise Http404
        ivs_client = boto3.client('ivs', region_name='us-west-2')
        response = ivs_client.get_stream_key(arn=channel.stream_key_arn)
        return Response(response.get('streamKey'))
        
    