from django.contrib import admin
from .models import User
from apps.checkout.admin import CartItemAdminInline
from apps.profiles.admin import AddressAdminInline

class UserAdmin(admin.ModelAdmin):
    inlines = [CartItemAdminInline, AddressAdminInline, ]

admin.site.register(User, UserAdmin)
