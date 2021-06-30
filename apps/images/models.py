from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

class Image16x16Mixin(models.Model):
    image_64x64= ImageSpecField(source='base', processors=[ResizeToFill(16, 16)], format='PNG', options={'quality': 70})
    class Meta:
        abstract = True

class Image24x24Mixin(models.Model):
    image_64x64= ImageSpecField(source='base', processors=[ResizeToFill(24, 24)], format='PNG', options={'quality': 70})
    class Meta:
        abstract = True

class Image32x32Mixin(models.Model):
    image_64x64= ImageSpecField(source='base', processors=[ResizeToFill(32, 32)], format='PNG', options={'quality': 70})
    class Meta:
        abstract = True

class Image48x48Mixin(models.Model):
    image_64x64= ImageSpecField(source='base', processors=[ResizeToFill(48, 48)], format='PNG', options={'quality': 70})
    class Meta:
        abstract = True


class Image96x96Mixin(models.Model):
    image_96x96= ImageSpecField(source='base', processors=[ResizeToFill(96, 96)], format='PNG', options={'quality': 70})
    class Meta:
        abstract = True

class Image128x128Mixin(models.Model):
    image_128x128 = ImageSpecField(source='base', processors=[ResizeToFill(128, 128)], format='PNG', options={'quality': 70})
    class Meta:
        abstract = True

class Image256x256Mixin(models.Model):
    image_256x256 = ImageSpecField(source='base', processors=[ResizeToFill(256, 256)], format='PNG', options={'quality': 70})
    class Meta:
        abstract = True

class Image512x512Mixin(models.Model):
    image_512x512 = ImageSpecField(source='base', processors=[ResizeToFill(512, 512)], format='PNG', options={'quality': 70})
    class Meta:
        abstract = True
