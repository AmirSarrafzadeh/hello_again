"""
Author: Amir Sarrafzadeh Arasi
Date: 2024-12-21

This script defines a Django custom management command to populate the database with three million random records across three related models: `Address`, `AppUser`, and `CustomerRelationship`. It uses the `Faker` library to generate realistic random data and optimizes database writes using bulk operations.

### Key Features:

1. **Command Definition**:
   - Implements the `BaseCommand` class, allowing the command to be run via `python manage.py populate_database`.

2. **Random Data Generation**:
   - Utilizes the `Faker` library to generate random but realistic data such as names, phone numbers, addresses, and dates.
   - Ensures the uniqueness of phone numbers by maintaining a set of used numbers.

3. **Bulk Insertion**:
   - Uses `bulk_create()` with a `batch_size` of 1000 to insert large volumes of data efficiently, reducing the overhead of individual `save()` calls.

4. **Models Populated**:
   - **Address**: Create three million records with randomly generated street names, city codes, cities, and countries.
   - **AppUser**: Links each user to a random address and generates random names, genders, unique customer IDs, and phone numbers.
   - **CustomerRelationship**: Links each record to a random user, with random loyalty points and activity timestamps.

5. **Execution Time Tracking**:
   - Records the start time and calculates the total time taken to populate the database, displaying it in minutes upon completion.

6. **Warning Suppression**:
   - Suppresses unnecessary warnings to keep the output clean.

7. **Error Prevention**:
   - Ensures uniqueness of phone numbers to avoid database constraint violations.
   - Randomly selects existing records for foreign key relationships (addresses for `AppUser` and users for `CustomerRelationship`).

### Usage:
1. Place the script in the `management/commands/` directory of the `loyalty_app`.
2. Run the command:
   ```bash
   python manage.py populate_database

"""
import os
import random
import logging
from faker import Faker
from pathlib import Path
from datetime import datetime
from logging.handlers import RotatingFileHandler
from django.core.management.base import BaseCommand
from loyalty_app.models import Address, AppUser, CustomerRelationship
import warnings
warnings.filterwarnings("ignore")

number_of_records = 3_000_000


class Command(BaseCommand):
    help = 'Populate the database with random data'

    def handle(self, *args, **kwargs):
        fake = Faker()
        start_time = datetime.now()
        # Build the BASE_DIR path for the project
        BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
        logs_path = os.path.join(BASE_DIR, 'logs')
        if not os.path.exists(logs_path):
            os.makedirs(logs_path)
        log_file_path = os.path.join(logs_path, 'populate_db.log')
        max_log_file_size = 512 * 1024 * 1024  # 512 MB
        handler = RotatingFileHandler(log_file_path, maxBytes=max_log_file_size, backupCount=5)
        # Configure logging
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[handler]
        )
        logging.info(f"Generating records started at {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

        try:
            # Insert Address records
            addresses = [
                Address(
                    street=fake.street_name(),
                    street_number=fake.building_number(),
                    city_code=fake.zipcode(),
                    city=fake.city(),
                    country=fake.country(),
                ) for _ in range(number_of_records)
            ]
            Address.objects.bulk_create(addresses, batch_size=1000)
        except Exception as e:
            logging.error(f"Error inserting Address records: {e}")
            return

        # Get all addresses
        addresses = list(Address.objects.all())

        # Use a set to keep track of unique phone numbers
        phone_numbers = set()
        users = []

        try:
            for _ in range(number_of_records):
                phone_number = fake.phone_number()[:15]

                # Ensure phone_number is unique
                while phone_number in phone_numbers:
                    phone_number = fake.phone_number()[:15]

                phone_numbers.add(phone_number)

                users.append(AppUser(
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    gender=random.choice(['Male', 'Female', 'Other']),
                    customer_id=fake.uuid4(),
                    phone_number=phone_number,
                    address=random.choice(addresses),
                    birthday=fake.date_of_birth(),
                ))

            AppUser.objects.bulk_create(users, batch_size=1000)
        except Exception as e:
            logging.error(f"Error inserting AppUser records: {e}")
            return

        # Get all users
        users = list(AppUser.objects.all())

        try:
            # Insert CustomerRelationship records
            relationships = [
                CustomerRelationship(
                    appuser=random.choice(users),
                    points=random.randint(0, 1000),
                    last_activity=fake.date_time_this_year(),
                ) for _ in range(number_of_records)
            ]
            CustomerRelationship.objects.bulk_create(relationships, batch_size=1000)
        except Exception as e:
            logging.error(f"Error inserting CustomerRelationship records: {e}")
            return

        logging.info(f"Database populated successfully within {(datetime.now() - start_time).seconds / 60} minutes.")
