# Generated by Django 3.2.5 on 2021-07-22 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShopbigChannels', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
