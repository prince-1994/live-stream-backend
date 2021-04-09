from django.db import models
from users.models import User
import os

class Channel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=100)
    stream_key = models.URLField()
    owner = models.ForeignKey(User, related_name="channels", on_delete=models.CASCADE)
    display_pic = models.FileField(null = True)
    background_pic = models.FileField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Video(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, null=True)
    channel = models.ForeignKey(Channel, related_name="videos", on_delete=models.CASCADE)
    mux_asset_id = models.URLField()

    def __str__(self):
        return self.name
