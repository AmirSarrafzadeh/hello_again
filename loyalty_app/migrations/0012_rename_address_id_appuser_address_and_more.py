# Generated by Django 5.1.4 on 2024-12-22 00:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loyalty_app', '0011_rename_address_appuser_address_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appuser',
            old_name='address_id',
            new_name='address',
        ),
        migrations.RenameField(
            model_name='customerrelationship',
            old_name='appuser_id',
            new_name='appuser',
        ),
    ]