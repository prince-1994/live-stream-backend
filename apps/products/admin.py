from django.contrib import admin
from .models import Category, Product, ProductImage

class ProductImageInlineAdmin(admin.StackedInline):
    model = ProductImage
    extra = 0

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInlineAdmin,]

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
