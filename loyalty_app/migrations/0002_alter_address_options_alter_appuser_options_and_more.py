# Generated by Django 5.1.4 on 2024-12-20 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loyalty_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='appuser',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='customerrelationship',
            options={'managed': True},
        ),
        migrations.AlterField(
            model_name='address',
            name='city_code',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='address',
            name='street_number',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='appuser',
            name='birthday',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterModelTable(
            name='address',
            table='address',
        ),
        migrations.AlterModelTable(
            name='appuser',
            table='appuser',
        ),
        migrations.AlterModelTable(
            name='customerrelationship',
            table='customerrelationship',
        ),
    ]
