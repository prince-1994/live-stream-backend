# Generated by Django 3.1.7 on 2021-06-05 18:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TslCloneShows', '0003_auto_20210605_1844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ivsvideo',
            name='show',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='video', to='TslCloneShows.show'),
        ),
    ]