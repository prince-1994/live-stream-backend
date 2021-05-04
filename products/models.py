from django.db import models
from channels.models import Channel

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
    channel = models.ForeignKey(Channel,related_name='products', on_delete=models.CASCADE)
    primary_image = models.ImageField(default=None)
    sku_id = models.CharField(max_length=100)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.PROTECT) 

    def __str__(self) -> str:
        return self.name

class ProductImage(models.Model):
    image = models.ImageField()
    product = models.ForeignKey(Product, related_name='productImages', on_delete=models.CASCADE)