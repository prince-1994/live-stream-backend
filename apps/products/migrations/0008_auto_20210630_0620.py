# Generated by Django 3.1.7 on 2021-06-30 06:20

from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('TslCloneProducts', '0007_auto_20210630_0614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sku_id',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
