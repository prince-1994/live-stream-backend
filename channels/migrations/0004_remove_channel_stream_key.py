# Generated by Django 3.1.7 on 2021-04-23 18:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('channels', '0003_auto_20210408_2226'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='channel',
            name='stream_key',
        ),
    ]
