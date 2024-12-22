# Hello Again - Loyalty App

<img src="https://i.postimg.cc/sD9s0Z6k/Slide2.jpg" alt="Photo">

## Overview

The **Hello Again - Loyalty App** is a Django-based application designed to manage users, their addresses, and customer relationships effectively. It provides powerful tools for dynamic filtering, sorting, and paginating data, making it ideal for CRM or loyalty program management systems. With robust logging and error handling, the app ensures reliability and scalability.

---

## Features

### 1. Dynamic Filtering
- Extracts filters from query parameters (`request.GET`).
- Supports case-insensitive exact matching (`iexact`) across fields in `AppUser`, `Address`, and `CustomerRelationship` models.
- Dynamically applies filters based on the presence of fields in models.

### 2. Sorting
- Enables sorting by any field specified in the query parameters.
- Supports both ascending (`asc`) and descending (`desc`) orders.

### 3. Pagination
- Uses Django's `Paginator` to handle large datasets.
- Allows customization of page size and navigation through `page` and `page_size` parameters.

### 4. Serialization
- Combines data from `AppUser`, `Address`, and `CustomerRelationship` models into a nested JSON response.
- Ensures compatibility with frontend applications.

### 5. Logging and Error Handling
- Implements `RotatingFileHandler` to manage log files efficiently.
- Logs incoming requests, parameter validation, filtering, sorting, and pagination processes.
- Gracefully handles errors with meaningful HTTP responses.

---

## Installation and Setup

### Used Technologies 
- Python 3.11.8
- Django 5.4.1
- PostgreSQL 17
- Redis 5.0.14
- Locust 2.32.4

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/AmirSarrafzadeh/hello_again.git
   ```
2. Navigate to the project directory:
   ```bash
   cd hello_again
   ```
3. If you would like to use a virtual environment, create and activate it:
   ```bash
   python -m venv venv
   source venv/scripts/activate
   ```
4. If you have Make installed, you can use the following commands to install the dependencies and run the server:
   ```bash
   make install
   make migrate
   make make
   make run
    ```
   in the case of needing help, you can use the following command:
   ```bash
    make help
    ```
5. If you don't have Make installed, you can install the dependencies manually:
    ```bash
    pip install -r requirements.txt
    ```
6. You should create a `.env` file in the root directory of the project and add the following variables:
    It should include the credentials for the database connection and secret key for Django.

7. Run the server:
   ```bash
   python manage.py runserver
   ```
8. Open your browser and navigate to `http://127.0.0.1:8000/` to access the app.

---

### For more information, please refer to the [API Documentation](http://127.0.0.1:8000/api/docs).

#### For checking the logs, you can navigate to the `logs` directory in the root of the project.

---
### Database Notes 
- The database is PostgreSQL, and you should have it installed on your machine.
- You should create a database named `hello_again` in your PostgreSQL.
- If you want, you can use the populate_db.py for populating the database with some random data.
- The number_of_records is set to 3_000_000 in the populate_db.py file, you can change it to any number you want.
- For populating the database, you can run the following command:
    ```bash
    python manage.py populate_db
    ```
  or if you have Make installed, you can use the following command:
    ```bash
    make pop
   ```
---
### Redis Notes
- The app uses Redis for caching the responses.
- You should have Redis installed on your machine.
- The default port for Redis is 6379.
- You can change the port in the settings.py file.
- The cache timeout is set to 30 minutes in the settings.py file, you can change it to any number you want.
---
### Logs Notes
- The app uses RotatingFileHandler for logging.
- The logs are stored in the logs directory in the root of the project.
- The Max Size of each log file is set to 512 MB with 5 backup files, you can change them as you want.
- Each log file is named with the specific script name.

# Developed with ❤️ by Amir 
