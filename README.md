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

### Prerequisites
- Python 3.8+
- Django 4.0+
- PostgreSQL

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/AmirSarrafzadeh/hello_again.git
   ```
2. Navigate to the project directory:
   ```bash
   cd hello_again
   ```

   







# Developed with ❤️ by Amir 
