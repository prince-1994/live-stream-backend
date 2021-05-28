from django.db import models
from django.db.models.aggregates import Max
from django.db.models.fields import related
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


class Order(models.Model):
    user = models.ForeignKey(User, related_name="orders", on_delete=models.PROTECT)
    stripe_payment_intent = models.CharField(max_length=100)
    paid_date = models.DateTimeField(null=True)
    total_amount = models.DecimalField(max_digits=10,decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class OrderItem(models.Model):
    product = models.ForeignKey(Product, related_name="product", on_delete=models.PROTECT)
    order = models.ForeignKey(Order, related_name="order_items", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    placed_date = models.DateTimeField(null=True)
    shipped_date = models.DateTimeField(null=True)
    delivered_date = models.DateTimeField(null=True)
    canceled_date = models.DateTimeField(null=True)
    settled_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(quantity__gte=1), name="order_item_quantity_gte_1")
        ]

class Customer(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    stripe_customer = models.CharField(max_length=100)
