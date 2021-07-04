from django.db import models
from apps.users.models import User
from apps.images.models import ImageAlbum

class Channel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    image_album = models.OneToOneField(ImageAlbum, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    arn = models.CharField( max_length=100,null=True, blank=True)
    stream_key_arn = models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return self.name

