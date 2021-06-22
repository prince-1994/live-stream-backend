from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import Show
from .serializers import IVSVideoSerializer, ShowSerializer
from .permissions import *
from apps.shows.constants import *
from apps.channels.models import Channel
from apps.shows.models import IVSVideo
import json
from django.http.response import Http404
from apps.products.models import Product
from apps.shows.serializers import WriteShowSerializer
from tslclone.permissions import ReadOnly
from apps.shows.views import VideoEditPermission, ShowEditPermission
from rest_framework.exceptions import PermissionDenied

class VideoViewSet(viewsets.ModelViewSet):
    serializer_class = IVSVideoSerializer
    permission_classes = (ReadOnly, VideoEditPermission)
    filterset_fields = {
        'show' : ['exact', 'isnull']
    }
    
    def get_queryset(self):
        channel = Channel.objects.filter(owner=self.request.user).first()
        if not channel:
            raise PermissionDenied("Channel does not exist")
        return IVSVideo.objects.filter(channel=channel)

class ShowViewSet(viewsets.ModelViewSet):
    serializer_class = ShowSerializer
    permission_classes = (ReadOnly|ShowEditPermission,)
    queryset = Show.objects.all()
    search_fields = ['name', 'description']
    filterset_fields = {
        'channel' : ['exact'],
        'video' : ['exact', 'isnull']
    }
    
    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return ShowSerializer
        else:
            return WriteShowSerializer

    def perform_create(self, serializer):
        user = self.request.user
        channel = Channel.objects.filter(owner=user).first()
        if not channel:
            raise PermissionDenied("channel does not exist")
        product_ids = set(product.id for product in Product.objects.filter(channel=channel))
        add_products = serializer.validated_data.pop('products')
        for product in add_products:
            if product.id not in product_ids:
                raise Http404("Product not found")
        obj = serializer.save(channel=channel)
        for product in add_products:
            obj.products.add(product)
        return super().perform_create(serializer)

    @action(detail=False, methods=['post'], permission_classes=(), url_path='videos/webhook')
    def webhook(self, request, *args, **kwargs):
        payload = json.loads(request.body)
        detail_type = payload["detail-type"]
        if detail_type == IVS_RECORDING_STATE_CHANGE_EVENT_TYPE:
            print(payload["resources"])
            channel = Channel.objects.get(arn=payload["resources"][0])
            detail = payload['detail']
            recording_status = detail[IVS_RECORDING_STATUS]
            handler = None
            try: 
                if recording_status == IVS_RECORDING_START_EVENT:
                    handler = self.handle_stream_recording_start
                elif recording_status == IVS_RECORDING_END_EVENT:
                    handler = self.handle_stream_recording_end
                elif recording_status == IVS_RECORDING_START_FAILURE_EVENT:
                    handler = self.handle_stream_recording_start_failed
                elif recording_status == IVS_RECORDING_END_FAILURE_EVENT:
                    handler = self.handle_stream_recording_end_failed
                handler(channel, detail) 
                return Response({"success" : "event was successfully handled"}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print(e)
                return Response({"error" : "event was not handled properly"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error" : "event not supported yet"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def handle_stream_recording_start(self, channel, data):
        found_videos = channel.videos.filter(aws_stream=data['stream_id'])
        if len(found_videos) > 0: return
        video = IVSVideo.objects.create(
            aws_stream=data['stream_id'],
            recording_status='S',
            s3_path=data['recording_s3_key_prefix'],
            s3_bucket = data['recording_s3_bucket_name'],
            channel = channel,
            recording_duration=data['recording_duration_ms']
        )
        video.save()

    def handle_stream_recording_start_failed(self, channel, data):
        found_videos = channel.videos.filter(aws_stream=data['stream_id'])
        if len(found_videos) > 0: return
        video = IVSVideo.objects.create(
            aws_stream=data['stream_id'],
            recording_status='SF',
            s3_bucket = data['recording_s3_bucket_name'],
            s3_path=None,
            channel = channel,
            recording_duration=data['recording_duration_ms']
        )
        video.save()

    def handle_stream_recording_end(self, channel, data):
        found_videos = channel.videos.filter(aws_stream=data['stream_id'])
        if len(found_videos) > 0:
            video = channel.videos.get(aws_stream=data['stream_id'])
            video.recording_status = 'E'
            video.recording_duration=data['recording_duration_ms']
        else :
            video = IVSVideo.objects.create(
                aws_stream=data['stream_id'],
                recording_status='E',
                s3_bucket = data['recording_s3_bucket_name'],
                s3_path=data['recording_s3_key_prefix'],
                channel = channel,
                recording_duration=data['recording_duration_ms']
            )
        video.save()
    
    def handle_stream_recording_end_failed(self, channel, data):
        found_videos = channel.videos.filter(aws_stream=data['stream_id'])
        if len(found_videos) > 0:
            video = channel.videos.get(aws_stream=data['stream_id'])
            video.recording_status = 'EF'
            video.recording_duration=data['recording_duration_ms']
        else :
            video = IVSVideo.objects.create(
                aws_stream=data['stream_id'],
                recording_status='EF',
                s3_bucket = data['recording_s3_bucket_name'],
                s3_path=data['recording_s3_key_prefix'],
                channel = channel,
                recording_duration=data['recording_duration_ms']
            )
        video.save()