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

    user = models.ForeignKey(User, related_name="orders", on_delete=models.PROTECT)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_payment_intent = models.CharField(max_length=100, default=None, null=True)
    payment_status = models.CharField(max_length=2, choices=PAYMENT_STATUS_CHOICES, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # can implement coupons for order

    def __str__(self) -> str:
        return f"Order #{self.id}"
    

class OrderItem(models.Model):
    product = models.ForeignKey(Product, related_name="order_items", on_delete=models.PROTECT)
    order = models.ForeignKey(Order, related_name="items", on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    commission = models.ForeignKey(Commission, related_name='order_items', on_delete=models.PROTECT)
    quantity = models.IntegerField()
    address = models.ForeignKey(Address, related_name="orders", on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(quantity__gte=1), name="order_item_quantity_gte_1")
        ]

    def __str__(self) -> str:
        return f"{self.product} ({self.quantity}) - {self.created_at}"

class OrderItemStatus(models.Model):
    STATUS_CHOICES = [
        ('P', 'placed'),
        ('C', 'canceled'),
        ('S', 'shipped'),
        ('D', 'delivered'),
    ]
    order_item = models.ForeignKey(OrderItem, related_name="statuses", on_delete=models.CASCADE)
    date = models.DateTimeField()
    value = models.CharField(max_length=1,choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('order_item', 'value',)

    def __str__(self) -> str:
        return f"{self.value} - {self.date}"