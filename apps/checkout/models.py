from django.db import models
from apps.users.models import User
from apps.products.models import Product


class CartItem(models.Model):
    user = models.ForeignKey(User, related_name='cart_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='products', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    
    class Meta:
        unique_together = [
            ['user', 'product']
        ]
        constraints = [
            models.CheckConstraint(check=models.Q(quantity__gte=1), name="cart_quantity_gte_1")
        ]

    def __str__(self):
        return f"{str(self.product)} ({self.quantity})" 