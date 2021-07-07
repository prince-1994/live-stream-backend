from django.db import models
from apps.users.models import User

class Address(models.Model):
    COUNTRY_CHOICES = [("IN", "India")]
    TYPE_CHOICES = [("H", "Home"), ("W", "Work")]
    user = models.ForeignKey(User, related_name="addresses", on_delete=models.CASCADE)
    type = models.CharField(max_length=100, choices=TYPE_CHOICES, default="H")
    name = models.CharField(max_length=100)
    line1 = models.CharField(max_length=200)
    line2 = models.CharField(max_length=200, null=True, blank=True)
    landmark = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, choices=COUNTRY_CHOICES)
    postal_code = models.CharField(max_length=20)
    phone_no = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name} ({self.type})"
