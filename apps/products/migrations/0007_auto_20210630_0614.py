# Generated by Django 3.1.7 on 2021-06-30 06:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TslCloneProducts', '0006_auto_20210630_0604'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image_album',
        ),
        migrations.RemoveField(
            model_name='productimage',
            name='album',
        ),
        migrations.AddField(
            model_name='productimage',
            name='product',
            field=models.ForeignKey(default=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='TslCloneProducts.product'),
        ),
    ]
