from apps.checkout.models import CartItem
from django.contrib import admin
from django.contrib.auth import models

class CartItemInline(admin.StackedInline):
    model = CartItem
    extra = 0
