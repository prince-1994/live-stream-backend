from apps.profiles.models import Address
from django.contrib import admin

class AddressAdminInline(admin.StackedInline):
    model = Address
    extra = 0
