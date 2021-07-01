from apps.checkout.models import CartItem, Order, OrderItem
from django.contrib import admin


class CartItemAdminInline(admin.StackedInline):
    model = CartItem
    extra = 0

admin.site.register(Order)
admin.site.register(OrderItem)
