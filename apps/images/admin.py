from django.contrib import admin
from apps.images.models import Image
from apps.images.models import ImageAlbum

class ImageAdminInline(admin.StackedInline):
    model = Image
    extra = 0

class ImageAlbumAdmin(admin.ModelAdmin):
    inlines = [ImageAdminInline, ]

admin.site.register(ImageAlbum, ImageAlbumAdmin)