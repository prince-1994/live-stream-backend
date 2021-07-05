from django.db import models
from apps.channels.models import Channel
from taggit.managers import TaggableManager
from apps.images.models import ImageAlbum

class  Category(models.Model):
    name = models.CharField(unique=True, max_length=150)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    channel = models.ForeignKey(Channel,related_name='products', on_delete=models.CASCADE, default=None)
    sku_id = models.CharField(max_length=100, blank=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    tags = TaggableManager(blank=True)
    image_album = models.OneToOneField(ImageAlbum, related_name='product', on_delete=models.CASCADE, default=None, null=True, blank=True)

    def __str__(self) -> str:
        return self.name
    