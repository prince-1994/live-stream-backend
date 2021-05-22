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