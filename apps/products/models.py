from django.db import models
from apps.channels.models import Channel
from taggit.managers import TaggableManager

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

    def __str__(self) -> str:
        return self.name

def base_image_name(instance, filename):
    user_id = instance.product.channel.user.id
    channel_id = instance.product.channel.id
    product_id = instance.product.id
    id = instance.id
    return f"users/{user_id}/channels/{channel_id}/products/{product_id}/images/{id}/filename"

class ProductImage(models.Model):
    image = models.ImageField(upload_to=base_image_name, default=None, null=True, blank=True)
    default = models.BooleanField(null=True, default=None, blank=True)
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)