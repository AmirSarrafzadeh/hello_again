"""
Author: Amir Sarrafzadeh Arasi
Date: 2024-12-21

This code defines three Django models that represent a data structure for a CRM-like application.

1. **Address Model**:
   - Represents address-related information such as street, street number, city code, city, and country.
   - It has a table name `address` and is managed by Django.

2. **AppUser Model**:
   - Represents users of the application with fields for first name, last name, gender (with predefined choices), unique customer ID, phone number, and associated address (via a foreign key to the `Address` model).
   - It also tracks the user's creation and last updated timestamps, along with an optional birthday field.
   - The table name is `appuser`, and it is managed by Django.

3. **CustomerRelationship Model**:
   - Represents a user's relationship details with fields for points, creation date, and last activity timestamp.
   - It has a foreign key linking it to the `AppUser` model.
   - The table name is `customerrelationship`, and it is managed by Django.

This structure allows the representation of users, their addresses, and their associated relationships, making it suitable for a CRM system.
"""

from django.db import models


class Address(models.Model):
    street = models.CharField(max_length=255)
    street_number = models.CharField(max_length=10)
    city_code = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    class Meta:
        db_table = 'address'
        managed = True


class AppUser(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    customer_id = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    birthday = models.DateField(blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'appuser'
        managed = True


class CustomerRelationship(models.Model):
    appuser = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    points = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField()

    class Meta:
        db_table = 'customerrelationship'
        managed = True
