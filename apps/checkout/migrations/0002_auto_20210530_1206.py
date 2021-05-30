# Generated by Django 3.1.7 on 2021-05-30 12:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TslCloneProducts', '0002_product_selling_price'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('TslCloneProfiles', '0003_customerprofile'),
        ('TslClonePayout', '0001_initial'),
        ('TslCloneCheckout', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_amount_collected', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_date', models.DateTimeField(null=True)),
                ('stripe_payment_intent', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('selling_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='TslCloneProfiles.address')),
                ('commission', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_items', to='TslClonePayout.commission')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_items', to='TslCloneCheckout.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_items', to='TslCloneProducts.product')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItemStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('value', models.CharField(choices=[('P', 'Placed'), ('C', 'Canceled'), ('S', 'Shipped'), ('D', 'Delivered')], max_length=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('order_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statuses', to='TslCloneCheckout.orderitem')),
            ],
        ),
        migrations.AddConstraint(
            model_name='orderitem',
            constraint=models.CheckConstraint(check=models.Q(quantity__gte=1), name='order_item_quantity_gte_1'),
        ),
    ]