# Generated by Django 3.0 on 2020-02-02 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cart', '0005_auto_20200201_0001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='total',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=20, null=True),
        ),
    ]
