# Generated by Django 3.1.7 on 2021-07-06 09:40

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
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('H', 'Home'), ('W', 'Work')], default='H', max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('line1', models.CharField(max_length=200)),
                ('line2', models.CharField(blank=True, max_length=200, null=True)),
                ('landmark', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('country', models.CharField(choices=[('IN', 'India')], max_length=100)),
                ('postal_code', models.CharField(max_length=20)),
                ('phone_no', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
