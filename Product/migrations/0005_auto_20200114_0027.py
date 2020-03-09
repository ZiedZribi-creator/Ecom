# Generated by Django 3.0 on 2020-01-13 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0004_auto_20200114_0024'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_variants',
            field=models.ManyToManyField(to='Product.ProductVariant'),
        ),
        migrations.AlterField(
            model_name='product',
            name='colors',
            field=models.ManyToManyField(to='Product.Color'),
        ),
    ]
