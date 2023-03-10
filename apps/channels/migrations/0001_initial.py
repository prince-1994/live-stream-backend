# Generated by Django 3.1.7 on 2021-07-06 09:41

import apps.channels.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('display_pic', models.ImageField(blank=True, default=None, null=True, upload_to=apps.channels.models.display_pic_name)),
                ('background_pic', models.ImageField(blank=True, default=None, null=True, upload_to=apps.channels.models.background_pic_name)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('arn', models.CharField(blank=True, max_length=100, null=True)),
                ('stream_key_arn', models.CharField(blank=True, max_length=100, null=True)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
