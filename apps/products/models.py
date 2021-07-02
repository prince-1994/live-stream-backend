from apps.images.models import Image128x128Mixin, Image512x512Mixin, Image96x96Mixin
from django.db import models
from apps.channels.models import Channel
from taggit.managers import TaggableManager
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit

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
    primary_image = models.ImageField(default=None)
    sku_id = models.CharField(max_length=100, blank=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    tags = TaggableManager(blank=True)

    def __str__(self) -> str:
        return self.name

class ProductImage(Image96x96Mixin, Image128x128Mixin, Image512x512Mixin):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE, null=True, default=True)
    base = models.ImageField()
    default = models.BooleanField(null=True, default=None, blank=True)
    