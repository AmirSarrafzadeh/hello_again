# Generated by Django 5.1.4 on 2024-12-21 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loyalty_app', '0009_alter_appuser_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='phone_number',
            field=models.CharField(max_length=40, unique=True),
        ),
    ]