from apps.products.models import Category
from django.db import models
from apps.channels.models import Channel

class Commission(models.Model):
    channel = models.ForeignKey(Channel, related_name="commissions", on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name="commissions", on_delete=models.CASCADE)
    percent_per_item = models.DecimalField(max_digits=3, decimal_places=2, default=5.0)
    fixed_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.channel.name} - {self.category.name} : {self.percent_per_item}% + {self.fixed_per_item}" 
