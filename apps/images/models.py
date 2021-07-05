from apps.users.models import User
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit

options = {'quality': 70}
format='PNG'
processors=[ResizeToFit(32, 32)]

# class Custorm

class Image32x32Mixin(models.Model):
    image_64x64= ImageSpecField(source='base', processors=[ResizeToFit(32, 32)], format='PNG', options=options)
    class Meta:
        abstract = True

class Image48x48Mixin(models.Model):
    image_64x64= ImageSpecField(source='base', processors=[ResizeToFit(48, 48)], format='PNG', options={'quality': 70})
    class Meta:
        abstract = True


class Image96x96Mixin(models.Model):
    image_96x96= ImageSpecField(source='base', processors=[ResizeToFit(96, 96)], format='PNG', options={'quality': 70})
    class Meta:
        abstract = True

class Image128x128Mixin(models.Model):
    image_128x128 = ImageSpecField(source='base', processors=[ResizeToFit(128, 128)], format='PNG', options={'quality': 70})
    class Meta:
        abstract = True

class Image256x256Mixin(models.Model):
    image_256x256 = ImageSpecField(source='base', processors=[ResizeToFit(256, 256)], format='PNG', options={'quality': 70})
    class Meta:
        abstract = True

class Image512x512Mixin(models.Model):
    image_512x512 = ImageSpecField(source='base', processors=[ResizeToFit(512, 512)], format='PNG', options={'quality': 70})
    class Meta:
        abstract = True

class Image180x320Mixin(models.Model):
    image_320x180 = ImageSpecField(source='base', processors=[ResizeToFit(180, 320)], format='PNG', options={'quality': 70})
    class Meta:
        abstract = True

class Image720x1280Mixin(models.Model):
    image_320x180 = ImageSpecField(source='base', processors=[ResizeToFit(720, 1280)], format='PNG', options={'quality': 70})
    class Meta:
        abstract = True

class ImageAlbum(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, related_name="images", on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.name

class Image(models.Model):
    base = models.ImageField()
    album = models.ForeignKey(ImageAlbum, related_name="images", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    default = models.BooleanField(null=True, default=None, blank=True)