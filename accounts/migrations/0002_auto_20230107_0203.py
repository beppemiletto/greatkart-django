# Generated by Django 3.1 on 2023-01-07 01:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='user',
            new_name='username',
        ),
    ]
