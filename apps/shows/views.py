from django.core.checks.messages import Error
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import Show
from .serializers import IVSVideoSerializer, ShowSerializer, EditShowSerializer
from .permissions import *
from apps.shows.constants import *
from apps.channels.models import Channel
from apps.shows.models import IVSVideo
import json
from datetime import datetime

class EditShowViewSet(viewsets.ModelViewSet):
    serializer_class = EditShowSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsShowOwner)

    def get_queryset(self):
        channel_id = self.kwargs['channel_id']
        return Show.objects.filter(channel__id = channel_id)

    @action(detail=False, methods=['GET'], permission_classes=(IsAuthenticatedOrReadOnly, IsShowOwner), url_path='without-video')
    def without_video(self, request, *args, **kwargs):
        all_shows = self.get_queryset()
        shows = all_shows.filter(video=None, time__lte=datetime.now())
        serializer = EditShowSerializer(shows, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class EditVideoViewSet(viewsets.ModelViewSet):
    serializer_class = IVSVideoSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsVideoOwner)
    
    def get_queryset(self):
        channel_id = self.kwargs['channel_id']
        return IVSVideo.objects.filter(channel__id = channel_id)

    @action(detail=False, methods=['GET'], permission_classes=(IsAuthenticatedOrReadOnly, IsVideoOwner), url_path='without-show')
    def videos_without_show(self, request, *args, **kwargs):
        videos = self.get_queryset()
        serializer = IVSVideoSerializer(videos)
        print(serializer.data)
        return Response(serializer.data)

class ShowViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ShowSerializer
    permission_classes = (AllowAny,)
    queryset = Show.objects.all()

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
        found_videos = channel.videos.filter(aws_stream_id=data['stream_id'])
        if len(found_videos) > 0: return
        video = IVSVideo.objects.create(
            aws_stream_id=data['stream_id'],
            recording_status='S',
            s3_path=data['recording_s3_key_prefix'],
            s3_bucket = data['recording_s3_bucket_name'],
            channel = channel,
            recording_duration=data['recording_duration_ms']
        )
        video.save()

    def handle_stream_recording_start_failed(self, channel, data):
        found_videos = channel.videos.filter(aws_stream_id=data['stream_id'])
        if len(found_videos) > 0: return
        video = IVSVideo.objects.create(
            aws_stream_id=data['stream_id'],
            recording_status='SF',
            s3_bucket = data['recording_s3_bucket_name'],
            s3_path=None,
            channel = channel,
            recording_duration=data['recording_duration_ms']
        )
        video.save()

    def handle_stream_recording_end(self, channel, data):
        found_videos = channel.videos.filter(aws_stream_id=data['stream_id'])
        if len(found_videos) > 0:
            video = channel.videos.get(aws_stream_id=data['stream_id'])
            video.recording_status = 'E'
            video.recording_duration=data['recording_duration_ms']
        else :
            video = IVSVideo.objects.create(
                aws_stream_id=data['stream_id'],
                recording_status='E',
                s3_bucket = data['recording_s3_bucket_name'],
                s3_path=data['recording_s3_bucket_name'],
                channel = channel,
                recording_duration=data['recording_duration_ms']
            )
        video.save()
    
    def handle_stream_recording_end_failed(self, channel, data):
        found_videos = channel.videos.filter(aws_stream_id=data['stream_id'])
        if len(found_videos) > 0:
            video = channel.videos.get(aws_stream_id=data['stream_id'])
            video.recording_status = 'EF'
            video.recording_duration=data['recording_duration_ms']
        else :
            video = IVSVideo.objects.create(
                aws_stream_id=data['stream_id'],
                recording_status='EF',
                s3_bucket = data['recording_s3_bucket_name'],
                s3_path=data['recording_s3_bucket_name'],
                channel = channel,
                recording_duration=data['recording_duration_ms']
            )
        video.save()