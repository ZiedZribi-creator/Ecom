# Generated by Django 3.0 on 2019-12-24 10:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Cart', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.CharField(choices=[('ordered', 'Just Ordered'), ('payed payme', 'Payed with payme'), ('payed cod', 'Payed with cod')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ShippingInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_type', models.CharField(choices=[('cod', 'COD'), ('payme', 'Payme')], max_length=50)),
                ('payed', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('runing', 'Runing'), ('shipped', 'Shipped')], max_length=50)),
                ('cart', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Cart.Cart')),
                ('history', models.ManyToManyField(to='Order.OrderHistory')),
                ('shipping_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Order.ShippingInfo')),
            ],
        ),
    ]
