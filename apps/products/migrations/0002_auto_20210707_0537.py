# Generated by Django 3.1.7 on 2021-07-07 05:37

import apps.products.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShopbigProducts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(blank=True, default=None, null=True, upload_to=apps.products.models.base_image_name),
        ),
    ]