"""
Author: Amir Sarrafzadeh Arasi
Date: 2024-12-21

This script implements a Django view function, `list_entries`, to dynamically list, filter, sort, and paginate data across three related models: `AppUser`, `Address`, and `CustomerRelationship`. It includes logging for debugging and error tracking.

### Key Features:

1. **Logging**:
   - Configures a `RotatingFileHandler` to manage log files (`file.log`) with a maximum size of 512 MB and up to 5 backup files.
   - Logs incoming requests, parameter validation, and potential errors during processing.

2. **Dynamic Filtering**:
   - Filters are extracted from the query parameters (`request.GET`).
   - Supports case-insensitive exact matching (`iexact`) across fields in `AppUser`, `Address`, and `CustomerRelationship`.
   - Dynamically applies filters by checking if the fields exist in the respective models.

3. **Sorting**:
   - Supports dynamic sorting by any field specified in the query parameter `sort_by`.
   - Accepts an optional `order` parameter (`asc` or `desc`) to define the sort direction.

4. **Pagination**:
   - Uses Django's `Paginator` to paginate results based on `page` and `page_size` query parameters.
   - Handles invalid or missing parameters gracefully with error logging.

5. **Serialization**:
   - Serializes `AppUser` data along with related `Address` and `CustomerRelationship` fields.
   - Constructs a nested JSON response for each entry, including user details, address information, and associated customer relationships.

6. **Error Handling**:
   - Handles errors gracefully during parameter extraction, filtering, sorting, and pagination.
   - Logs detailed error messages and returns appropriate HTTP error responses (`400 Bad Request`).

7. **JSON Response**:
   - Returns a structured JSON response containing paginated results, total pages, and total items, ensuring compatibility with frontend applications.

### Example Use Case:
This function can be used in a CRM-like application where administrators need to search, filter, and manage large datasets of users, their addresses, and loyalty relationships dynamically and efficiently.
"""
# Import the necessary modules and libraries
import os
import logging
from pathlib import Path
from django.db.models import Prefetch
from django.http import JsonResponse
from django.core.paginator import Paginator
from logging.handlers import RotatingFileHandler
from loyalty_app.models import AppUser, Address, CustomerRelationship

# Initialize a logger for this module
logger = logging.getLogger(__name__)
log_file_size = 512 * 1024 * 1024  # 512 MB
BASE_DIR = Path(__file__).resolve().parent.parent
logs_path = os.path.join(BASE_DIR, 'logs')

if not os.path.exists(logs_path):
    os.makedirs(logs_path)

log_file_path = os.path.join(logs_path, 'views.log')
file_handler = RotatingFileHandler(log_file_path, maxBytes=log_file_size, backupCount=5)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

def list_entries(request):
    """
    Lists entries from AppUser, Address, and CustomerRelationship.
    Includes filtering, sorting, and pagination.
    """
    logger.info("Incoming request to entries endpoint with parameters: %s", request.GET.dict())

    try:
        # Get filter and sort parameters
        filters = {key: value for key, value in request.GET.items() if key not in ["sort_by", "order", "page", "page_size"]}
        sort_by = request.GET.get("sort_by", "id")
        order = request.GET.get("order", "asc")
        page = int(request.GET.get("page", 1))
        page_size = int(request.GET.get("page_size", 10))
        logger.info("Parameters extracted successfully")
    except ValueError:
        logger.error("Invalid query parameters")
        return JsonResponse({"error": "Invalid query parameters"}, status=400)

    # Validate sort order
    if order == "desc":
        sort_by = f"-{sort_by}"

    # Build the base queryset
    queryset = AppUser.objects.select_related("address").prefetch_related(
        Prefetch("customerrelationship_set")
    )

    # Apply filtering dynamically with case-insensitive exact match
    try:
        for field, value in filters.items():
            if hasattr(AppUser, field):  # Check if AppUser has the field
                queryset = queryset.filter(**{f"{field}__iexact": value})
                logger.debug("Filtering AppUser by %s: %s", field, value)
            elif hasattr(Address, field):  # Check if the Address has the field
                queryset = queryset.filter(**{f"address__{field}__iexact": value})
                logger.debug("Filtering Address by %s: %s", field, value)
            elif hasattr(CustomerRelationship, field):  # Check if CustomerRelationship has the field
                queryset = queryset.filter(**{f"customerrelationship__{field}__iexact": value})
                logger.debug("Filtering CustomerRelationship by %s: %s", field, value)
    except Exception as e:
        logger.error("Error applying filters: %s", e)
        return JsonResponse({"error": "Error applying filters"}, status=400)

    try:
        # Apply sorting
        queryset = queryset.order_by(sort_by)

        # Paginate results
        paginator = Paginator(queryset, page_size)
        paginated_data = paginator.get_page(page)
    except Exception as e:
        logger.error("Error applying sorting or pagination: %s", e)
        return JsonResponse({"error": "Error applying sorting or pagination"}, status=400)

    # Serialize data
    results = []
    try:
        for app_user in paginated_data:
            results.append(
                {
                    "id": app_user.id,
                    "first_name": app_user.first_name,
                    "last_name": app_user.last_name,
                    "gender": app_user.gender,
                    "phone_number": app_user.phone_number,
                    "address": {
                        "street": app_user.address.street,
                        "street_number": app_user.address.street_number,
                        "city_code": app_user.address.city_code,
                        "city": app_user.address.city,
                        "country": app_user.address.country,
                    },
                    "customer_relationships": [
                        {
                            "points": relationship.points,
                            "created": relationship.created,
                            "last_activity": relationship.last_activity,
                        }
                        for relationship in app_user.customerrelationship_set.all()
                    ],
                }
            )
    except Exception as e:
        logger.error("Error in for loop in serializing data: %s", e)
        return JsonResponse({"error": "Error serializing data"}, status=500)

    # Return JSON response
    return JsonResponse(
        {
            "page": page,
            "total_pages": paginator.num_pages,
            "total_items": paginator.count,
            "results": results,
        }
    )
