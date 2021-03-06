# Generated by Django 3.0 on 2020-01-30 22:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0012_product_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientproduct',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='clientproduct',
            name='color',
        ),
        migrations.RemoveField(
            model_name='clientproduct',
            name='nb',
        ),
        migrations.RemoveField(
            model_name='clientproduct',
            name='size',
        ),
        migrations.RemoveField(
            model_name='clientproduct',
            name='whishlist',
        ),
        migrations.AddField(
            model_name='clientproduct',
            name='qty',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='clientproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Product.Product'),
        ),
    ]
