# Generated by Django 5.1.4 on 2024-12-21 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loyalty_app', '0003_alter_address_city_alter_address_country_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='country',
            field=models.CharField(max_length=50),
        ),
    ]