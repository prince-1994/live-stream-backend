from django.db import models
from apps.users.models import User

class Channel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    display_pic = models.ImageField(null = True)
    background_pic = models.ImageField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    arn = models.CharField( max_length=100,null=True)
    stream_key_arn = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.name

