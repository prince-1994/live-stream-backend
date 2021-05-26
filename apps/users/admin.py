from django.contrib import admin
from .models import User
from apps.checkout.admin import CartItemInline

class UserAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]

admin.site.register(User, UserAdmin)
