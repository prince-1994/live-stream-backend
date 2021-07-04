from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.shows.models import Show, IVSStream
from .serializers import IVSStreamSerializer, ShowSerializer
from rest_framework import permissions
from apps.shows.constants import *
from apps.channels.models import Channel
import json
from apps.shows.serializers import WriteShowSerializer
from core.permissions import ReadOnly
from apps.shows.permissions import VideoEditPermission, ShowEditPermission
from rest_framework.exceptions import PermissionDenied
import dateutil.parser
from datetime import timedelta

def get_stream(channel, aws_stream_id, create=False):
    stream = channel.streams.filter(aws_stream_id=aws_stream_id).first()
    if create and (not stream):
        stream = IVSStream.objects.create(channel=channel, aws_stream_id=aws_stream_id)
    return stream


def save_recording_data(stream, data, status):
    for item in IVSStream.RECORDING_STATUS_CHOICES:
        if item[1] == status:
            stream.recording_status = item[0]
            break
    stream.s3_path = data.get("recording_s3_key_prefix")
    stream.s3_bucket = data.get("recording_s3_bucket_name")
    stream.recording_duration = data.get("recording_duration_ms")
    stream.save()


def get_ivs_stream_event_handler(event, event_type):
    if event_type == IVS_RECORDING_STATE_CHANGE_EVENT_TYPE:

        def recording_event_handler(channel, data, time):
            if not status:
                raise Exception("Event not supported")
            aws_stream_id = data.get("stream_id")
            stream = get_stream(channel, aws_stream_id, create=True)
            save_recording_data(stream, data, event)

        return recording_event_handler

    elif event_type == IVS_STREAM_STATE_CHANGE_EVENT_TYPE:

        def stream_change_event_handler(channel, data, time):
            aws_stream_id = data.get("stream_id")
            stream = get_stream(channel, aws_stream_id, create=True)
            if event == IVS_STREAM_START_EVENT:
                if stream.is_live == None:
                    stream.is_live = True
                stream.start_time = time
                time_delta = timedelta(minutes=SHOW_TIME_DELTA)
                show = channel.shows.filter(
                    time__gte=time - time_delta,
                    time__lte=time + time_delta,
                    stream=None,
                ).first()
                if show:
                    stream.show = show
            elif event == IVS_STREAM_END_EVENT:
                stream.is_live = False
                stream.end_time = time
            else:
                raise Exception("Event not supported")
            stream.save()

        return stream_change_event_handler
    else:
        return None


class StreamViewSet(viewsets.ModelViewSet):
    serializer_class = IVSStreamSerializer
    permission_classes = (VideoEditPermission,)
    filterset_fields = {
        "show": ["exact", "isnull"],
    }

    def get_queryset(self):
        channel = Channel.objects.filter(owner=self.request.user).first()
        if not channel:
            raise PermissionDenied("Channel does not exist")
        return IVSStream.objects.filter(channel=channel)

    @action(detail=False, methods=["post"], permission_classes=())
    def webhook(self, request, *args, **kwargs):
        payload = json.loads(request.body)
        print(payload)
        detail_type = payload["detail-type"]
        print(payload.get("time"))
        time = dateutil.parser.isoparse(payload.get("time"))
        channel = Channel.objects.get(arn=payload["resources"][0])
        detail = payload["detail"]
        event_name = None
        if detail_type == IVS_RECORDING_STATE_CHANGE_EVENT_TYPE:
            event_name = detail[IVS_RECORDING_STATUS]
        elif detail_type == IVS_STREAM_STATE_CHANGE_EVENT_TYPE:
            event_name = detail[IVS_STREAM_EVENT_NAME]
        handler = get_ivs_stream_event_handler(event_name, detail_type)
        if handler:
            try:
                handler(channel, detail, time)
                return Response(
                    {"success": "event was successfully handled"},
                    status=status.HTTP_202_ACCEPTED,
                )
            except Exception as e:
                print(e)
                return Response(
                    {"error": "event was not handled properly"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        else:
            return Response(
                {"error": "event handler not found"}, status=status.HTTP_400_BAD_REQUEST
            )


class ShowViewSet(viewsets.ModelViewSet):
    serializer_class = ShowSerializer
    permission_classes = (ReadOnly | ShowEditPermission,)
    queryset = Show.objects.all()
    search_fields = ["name", "description"]
    filterset_fields = {
        "channel": ["exact"],
        "stream": ["exact", "isnull"],
        "stream__is_live": ["exact"],
        "time": ["gte", "lte"],
    }
    ordering_fields = ['-time']

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return ShowSerializer
        else:
            return WriteShowSerializer

