# Generated by Django 3.0 on 2020-01-30 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0014_auto_20200130_2330'),
        ('Cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='product',
            field=models.ManyToManyField(to='Product.ClientProduct'),
        ),
    ]
