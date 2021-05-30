# Generated by Django 3.1.7 on 2021-05-30 12:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('TslCloneProfiles', '0002_address_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_profile', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='customer_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]