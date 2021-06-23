from os import read
from apps.payout.models import Commission
from apps.profiles.models import Address
from django.db import models
from apps.users.models import User
from apps.products.models import Product
from apps.channels.models import Channel


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
    PAYMENT_STATUS_CHOICES = [
        ('cn', 'canceled'),
        ('cr', 'created'),
        ('fa', 'failed'),
        ('pr', 'processing'),
        ('ra', 'requires_action'),
        ('sc', 'succeeded'),
    ]

    user = models.ForeignKey(User, related_name="orders", on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_payment_intent = models.CharField(max_length=100, default=None, null=True, blank=True)
    payment_status = models.CharField(max_length=2, choices=PAYMENT_STATUS_CHOICES, null=True, default=None, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # can implement coupons for order

    def __str__(self) -> str:
        return f"Order #{self.id}"
    

class OrderItem(models.Model):
    STATUS_CHOICES = [
        ('P', 'placed'),
        ('C', 'canceled'),
        ('S', 'shipped'),
        ('D', 'delivered'),
    ]

    product = models.ForeignKey(Product, related_name="order_items", on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    commission = models.ForeignKey(Commission, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    address = models.ForeignKey(Address, related_name="orders", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1,choices=STATUS_CHOICES, default='P')
    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(quantity__gte=1), name="order_item_quantity_gte_1")
        ]

    def __str__(self) -> str:
        return f"{self.product} ({self.quantity}) - {self.created_at}"