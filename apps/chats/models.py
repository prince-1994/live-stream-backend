from typing import ContextManager
from apps.users.models import User
from apps.shows.models import Show
from django.db import models


class Message(models.Model):
    show=models.ForeignKey(Show, related_name="messages", on_delete=models.CASCADE)
    user=models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content= models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.content}"