# Generated by Django 3.0 on 2020-01-11 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0002_auto_20200111_2037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorie',
            name='subcategorie',
            field=models.ManyToManyField(blank=True, null=True, to='Product.SubCategorie'),
        ),
        migrations.AlterField(
            model_name='section',
            name='categorie',
            field=models.ManyToManyField(blank=True, null=True, to='Product.Categorie'),
        ),
    ]
