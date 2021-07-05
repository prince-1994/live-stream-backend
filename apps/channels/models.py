from django.db import models
from django.utils import tree
from apps.users.models import User
from apps.images.models import ImageAlbum

class Channel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    display_pic_album = models.OneToOneField(ImageAlbum, related_name='display_pic_channel', on_delete=models.CASCADE, default=None, null=True, blank=True)
    background_pic_album = models.OneToOneField(ImageAlbum, related_name='background_pic_channel', on_delete=models.CASCADE, default=None, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    arn = models.CharField( max_length=100,null=True, blank=True)
    stream_key_arn = models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return self.name

