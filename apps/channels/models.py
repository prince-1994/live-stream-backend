from django.db import models
from django.utils import tree
from apps.users.models import User

def display_pic_name(instance, filename):
    user_id = instance.owner.id
    channel_id = instance.id
    return f"users/{user_id}/channels/{channel_id}/display_pic/{filename}"

def background_pic_name(instance, filename):
    user_id = instance.owner.id
    channel_id = instance.id
    return f"users/{user_id}/channels/{channel_id}/display_pic/{filename}"

class Channel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    display_pic = models.ImageField(upload_to=display_pic_name, default=None, null=True, blank=True)
    background_pic = models.ImageField(upload_to=background_pic_name,  default=None, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    arn = models.CharField( max_length=100,null=True, blank=True)
    stream_key_arn = models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return self.name

