# Generated by Django 3.0 on 2020-01-30 23:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Cart', '0003_auto_20200130_2343'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='product',
            new_name='products',
        ),
    ]
