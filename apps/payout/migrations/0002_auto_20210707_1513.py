# Generated by Django 3.1.7 on 2021-07-07 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShopbigPayout', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commission',
            name='fixed_per_item',
            field=models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=10),
        ),
        migrations.AlterField(
            model_name='commission',
            name='percent_per_item',
            field=models.DecimalField(decimal_places=2, default=5.0, editable=False, max_digits=3),
        ),
    ]