# Generated by Django 3.1.7 on 2021-07-05 11:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ShopbigImages', '0005_auto_20210705_1149'),
        ('ShopbigProducts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImageAlbumSerializer',
            fields=[
                ('imagealbum_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ShopbigImages.imagealbum')),
            ],
            bases=('ShopbigImages.imagealbum',),
        ),
        migrations.AddField(
            model_name='product',
            name='image_album',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product', to='ShopbigImages.imagealbum'),
        ),
    ]
