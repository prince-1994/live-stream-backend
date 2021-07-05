from apps.shows.constants import IVS_RECORDING_END_EVENT, IVS_RECORDING_END_FAILURE_EVENT, IVS_RECORDING_START_EVENT, IVS_RECORDING_START_FAILURE_EVENT
from django.db import models
from apps.channels.models import Channel
from apps.products.models import Product

def display_pic_name(instance, filename) :
    user_id = instance.channel.owner.id
    channel_id = instance.channel.id
    show_id = instance.id
    return f"users/{user_id}/channels/{channel_id}/shows/{show_id}/display_pic/{filename}"


class Show(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    channel = models.ForeignKey(Channel, related_name="shows", on_delete=models.CASCADE)
    display_pic = models.ImageField(upload_to=display_pic_name, default=None, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    time = models.DateTimeField()
    products = models.ManyToManyField(Product)

    def __str__(self):
        return self.name

class IVSStream(models.Model):
    RECORDING_STATUS_CHOICES=[
        ('S', IVS_RECORDING_START_EVENT),
        ('E', IVS_RECORDING_END_EVENT),
        ('SF', IVS_RECORDING_START_FAILURE_EVENT),
        ('EF', IVS_RECORDING_END_FAILURE_EVENT)
    ]
    aws_stream_id = models.CharField(max_length=100)
    is_live = models.BooleanField(default=None, null=True, blank=True)
    start_time = models.DateTimeField(default=None, null=True, blank=True)
    end_time = models.DateTimeField(default=None, null=True, blank=True)
    recording_duration = models.IntegerField(default=None, null=True, blank=True)
    recording_status = models.CharField(max_length=2, choices=RECORDING_STATUS_CHOICES, null=True, default=None, blank=True)
    show = models.OneToOneField(Show, related_name="stream", on_delete=models.CASCADE, null=True, default=None, blank=True)
    channel=models.ForeignKey(Channel, related_name="streams", on_delete=models.CASCADE)
    s3_path=models.CharField(max_length=200, null=True, blank=True)
    s3_bucket=models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.channel.name} - {self.aws_stream_id}"