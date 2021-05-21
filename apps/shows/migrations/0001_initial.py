# Generated by Django 3.1.7 on 2021-05-21 07:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('TslCloneProducts', '0001_initial'),
        ('TslCloneChannels', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('display_pic', models.ImageField(default=None, upload_to='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('time', models.DateTimeField()),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shows', to='TslCloneChannels.channel')),
                ('products', models.ManyToManyField(to='TslCloneProducts.Product')),
            ],
        ),
    ]
