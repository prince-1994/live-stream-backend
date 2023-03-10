from django.http.response import Http404
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .models import Channel
from .serializers import ChannelSerializer
from .permissions import *
import boto3
from core.permissions import ReadOnly
from apps.channels.permissions import ChannelEditPermission
from rest_framework.decorators import action
from django.conf import settings


class ChannelViewSet(viewsets.ModelViewSet):
    serializer_class = ChannelSerializer
    permission_classes = (ReadOnly | ChannelEditPermission,)
    search_fields = ["name", "description"]
    filterset_fields = ["owner"]
    queryset = Channel.objects.all()

    def perform_destroy(self, instance):
        ivs_client = boto3.client(
            "ivs",
            region_name="us-west-2",
            aws_access_key_id=settings.AWS_IVS_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_IVS_SECRET_KEY,
        )
        ivs_client.delete_channel(arn=instance.arn)
        return super().perform_destroy(instance)

    @action(detail=False, methods=["get"], permission_classes=(), url_path="detail")
    def get_aws_channel(self, request):
        channel = Channel.objects.filter(owner=request.user).first()
        if not channel:
            raise Http404
        ivs_client = boto3.client(
            "ivs",
            region_name="us-west-2",
            aws_access_key_id=settings.AWS_IVS_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_IVS_SECRET_KEY,
        )
        response = ivs_client.get_channel(arn=channel.arn)
        return Response(response.get("channel"))

    @action(
        detail=False, methods=["get"], permission_classes=(), url_path="stream-detail"
    )
    def get_aws_stream(self, request):
        channel = Channel.objects.filter(owner=request.user).first()
        if not channel:
            raise Http404
        ivs_client = boto3.client(
            "ivs",
            region_name="us-west-2",
            aws_access_key_id=settings.AWS_IVS_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_IVS_SECRET_KEY,
        )
        try:
            response = ivs_client.get_stream(channelArn=channel.arn)
            return Response(response.get("stream"))
        except:
            return Response(
                {"stream": "No live stream is present"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

    @action(
        detail=False,
        methods=["get"],
        permission_classes=(IsAuthenticated,),
        url_path="stream-key",
    )
    def get_aws_stream_key(self, request):
        channel = Channel.objects.filter(owner=request.user).first()
        if not channel:
            raise Http404
        ivs_client = boto3.client(
            "ivs",
            region_name="us-west-2",
            aws_access_key_id=settings.AWS_IVS_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_IVS_SECRET_KEY,
        )
        response = ivs_client.get_stream_key(arn=channel.stream_key_arn)
        return Response(response.get("streamKey"))
