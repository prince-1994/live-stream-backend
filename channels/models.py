from django.db import models
from users.models import User

class Channel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey(User, related_name="channels", on_delete=models.CASCADE, unique=True)
    display_pic = models.ImageField(null = True)
    background_pic = models.ImageField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.name

