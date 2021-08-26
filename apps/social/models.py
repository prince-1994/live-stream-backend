from django.db import models
from apps.channels.models import Channel


class Social(models.Model):
    SOCIAL_ACCOUNT_TYPES = [("FB", "FACEBOOK"), ("YT", "YOUTUBE"), ("CUS", "CUSTOM")]
    rtmp_ingest = models.CharField(max_length=500)
    rtmp_key = models.CharField(max_length=200)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=5, choices=SOCIAL_ACCOUNT_TYPES)
    channel = models.ForeignKey(
        Channel, related_name="socials", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
