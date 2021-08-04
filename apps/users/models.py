from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import BLANK_CHOICE_DASH
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from .managers import CustomUserManager

def profile_pic_name(instance, filename):
    return f"users/{instance.id}/profile_pic/{filename}"

class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    profile_pic = models.ImageField(default=None, null=True, blank=True, upload_to=profile_pic_name)
    stripe_customer = models.CharField(max_length=100, null = True, blank=True)
    stripe_connected_account = models.CharField(max_length=100, null=True, blank=True)
    seller_activated = models.BooleanField(default=settings.SHOPBIG_ALLOW_SELLERS_BY_DEFAULT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

