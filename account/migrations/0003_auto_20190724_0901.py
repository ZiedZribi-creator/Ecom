# Generated by Django 2.0 on 2019-07-24 08:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_remove_profile_summary'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Profile',
            new_name='DoctorProfile',
        ),
    ]
