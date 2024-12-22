"""
Author: Amir Sarrafzadeh Arasi
Date: 2024-12-21

This script defines a Locust test class, `BenchmarkUser`, to simulate load testing for a Django application's `entries` endpoint. The class uses Locust's `HttpUser` to perform HTTP requests to the application and measures its performance under different scenarios.

### Key Features:

1. **Configuration**:
   - The `host` is set to `http://127.0.0.1:8000`, indicating the local Django development server.
   - The `wait_time` is defined as a random interval between 1 and 2 seconds to simulate user-like behavior and avoid constant requests.

2. **Tasks**:
   - **`filter_by_name`**:
     - Sends a GET request to `/entries` with a query parameter `name=John`.
     - Tests the endpoint's ability to filter results by the `first_name` field.
   - **`sort_by_attribute`**:
     - Sends a GET request to `/entries/` with query parameters `sort_by=last_name&order=asc`.
     - Tests the endpoint's sorting functionality based on the `last_name` attribute in ascending order.
   - **`load_paginated_list`**:
     - Sends a GET request to `/entries/` with query parameters `page=1&page_size=100`.
     - Tests the endpoint's pagination mechanism, ensuring it can handle large datasets effectively.
    - **`filter_by_birthday`**:
     - Sends a GET request to `/entries` with a query parameter `birthday=1960-10-27`.
     - Tests the endpoint's ability to filter results by the `birthday` field.

3. **Task Weighting**:
   - Each task has an equal weight (`@task(1)`), meaning all tasks are executed with the same probability during the load test.
   - The weights can be adjusted to prioritize specific tasks for performance testing.

4. **Scalability**:
   - This class can be extended with additional tasks to test other functionalities or scenarios.
   - Supports scaling with multiple concurrent users for stress testing.

### Usage:
1. Save this script as `locustfile.py`.
2. Run Locust:
   ```bash
   locust -f locustfile.py
   ```
"""

from locust import HttpUser, task, between


class BenchmarkUser(HttpUser):
    wait_time = between(1, 2)
    host = "http://127.0.0.1:8000"

    @task(1)
    def filter_by_first_name(self):
        self.client.get("/entries?country=Italy")

    @task(1)
    def sort_by_attribute(self):
        self.client.get("/entries?sort_by=customerrelationship__points&order=asc")

    @task(1)
    def load_paginated_list(self):
        self.client.get("/entries?page=1&page_size=100")

    @task(1)
    def filter_by_birthday(self):
        self.client.get("/entries?birthday=1960-10-27")
