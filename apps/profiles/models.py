from django.db import models
from apps.users.models import User

class Address(models.Model):
    user = models.ForeignKey(User, related_name="addresses", on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default="home")
    name = models.CharField(max_length=100)
    first_line = models.CharField(max_length=200)
    second_line = models.CharField(max_length=200, null=True)
    landmark = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    phone_no= models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, related_name="customer_profile", on_delete=models.PROTECT)
    stripe_profile = models.CharField(max_length=100)