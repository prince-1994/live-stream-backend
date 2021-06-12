from botocore import model
from django.db import models
from apps.channels.models import Channel
from apps.products.models import Product

class Show(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    channel = models.ForeignKey(Channel, related_name="shows", on_delete=models.CASCADE)
    display_pic = models.ImageField(default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    time = models.DateTimeField()
    products = models.ManyToManyField(Product)

    def __str__(self):
        return self.name

class IVSVideo(models.Model):
    RECORDING_STATUS_CHOICES=[
        ('S', 'Started'),
        ('E', 'Ended'),
        ('SF', 'Start Failed'),
        ('EF', 'End Failed')
    ]
    aws_stream = models.CharField(max_length=100)
    recording_duration = models.IntegerField()
    recording_status = models.CharField(max_length=2, choices=RECORDING_STATUS_CHOICES)
    show = models.OneToOneField(Show, related_name="video", on_delete=models.CASCADE, null=True, default=None, blank=True)
    channel=models.ForeignKey(Channel, related_name="videos", on_delete=models.CASCADE)
    s3_path=models.CharField(max_length=200, null=True, blank=True)
    s3_bucket=models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.channel.name} - {self.aws_stream}"