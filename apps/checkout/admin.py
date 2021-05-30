from apps.checkout.models import CartItem, Order, OrderItem, OrderItemStatus
from django.contrib import admin


class CartItemAdminInline(admin.StackedInline):
    model = CartItem
    extra = 0

class OrderItemStatusAdminInline(admin.StackedInline):
    model = OrderItemStatus
    extra = 0

class OrderItemAdmin(admin.ModelAdmin):
    inlines = [OrderItemStatusAdminInline,]

admin.site.register(Order)
admin.site.register(OrderItem, OrderItemAdmin)
