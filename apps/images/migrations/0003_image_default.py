# Generated by Django 3.1.7 on 2021-07-05 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShopbigImages', '0002_image_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='default',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
    ]
