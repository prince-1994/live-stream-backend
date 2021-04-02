from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import related

class UserProfile(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) :
        return f"{self.first_name} {self.last_name}"

class Channel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=100)
    stream = models.URLField()
    user = models.ForeignKey(User, related_name="channels", on_delete=models.CASCADE)
    display_pic = models.FileField(null = True)
    background_pic = models.FileField(null=True)

    def __str__(self):
        return self.name

class Video(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField()
    thumbnail = models.FileField(null=True)
    name = models.CharField(max_length=100, null=True)
    channel = models.ForeignKey(Channel, related_name="videos", on_delete=models.CASCADE)
