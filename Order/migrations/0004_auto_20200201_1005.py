# Generated by Django 3.0 on 2020-02-01 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0003_auto_20200201_0001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('runing', 'Runing'), ('shipped', 'Shipped')], default='Runing', max_length=50),
        ),
    ]
