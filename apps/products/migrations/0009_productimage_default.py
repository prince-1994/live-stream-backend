# Generated by Django 3.1.7 on 2021-06-30 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TslCloneProducts', '0008_auto_20210630_0620'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimage',
            name='default',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
    ]