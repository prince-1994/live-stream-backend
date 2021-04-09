from django.db import models
from users.models import User

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

class ProductImage(models.Model):
    image = models.ImageField()
    product = models.ForeignKey(Product, related_name='productImages', on_delete=models.CASCADE)