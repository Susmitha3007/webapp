# Generated by Django 5.0.6 on 2024-05-25 06:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='destination',
            old_name='http',
            new_name='http_method',
        ),
    ]