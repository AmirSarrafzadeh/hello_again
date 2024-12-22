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
    Includes filtering, sorting, and pagination with support for date filters and exact date queries.
    """
    logger.info("Incoming request to entries endpoint with parameters: %s", request.GET.dict())

    try:
        # Extract filter and sort parameters
        filters = {key: value for key, value in request.GET.items() if
                   key not in ["sort_by", "order", "page", "page_size",
                               "created", "created_after", "created_before",
                               "last_updated", "last_updated_after", "last_updated_before",
                               "last_activity", "last_activity_after", "last_activity_before"]}
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

    # Apply filtering dynamically with case-insensitive exact match and date filters
    try:
        # Standard filters
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

        # Date filters: Exact and Ranges
        created = request.GET.get("created")
        created_after = request.GET.get("created_after")
        created_before = request.GET.get("created_before")
        if created:
            queryset = queryset.filter(created=created)
            logger.debug("Filtering by exact created date: %s", created)
        if created_after:
            queryset = queryset.filter(created__gte=created_after)
            logger.debug("Filtering by created_after: %s", created_after)
        if created_before:
            queryset = queryset.filter(created__lte=created_before)
            logger.debug("Filtering by created_before: %s", created_before)

        last_updated = request.GET.get("last_updated")
        last_updated_after = request.GET.get("last_updated_after")
        last_updated_before = request.GET.get("last_updated_before")
        if last_updated:
            queryset = queryset.filter(last_updated=last_updated)
            logger.debug("Filtering by exact last_updated date: %s", last_updated)
        if last_updated_after:
            queryset = queryset.filter(last_updated__gte=last_updated_after)
            logger.debug("Filtering by last_updated_after: %s", last_updated_after)
        if last_updated_before:
            queryset = queryset.filter(last_updated__lte=last_updated_before)
            logger.debug("Filtering by last_updated_before: %s", last_updated_before)

        last_activity = request.GET.get("last_activity")
        last_activity_after = request.GET.get("last_activity_after")
        last_activity_before = request.GET.get("last_activity_before")
        if last_activity:
            queryset = queryset.filter(customerrelationship__last_activity=last_activity)
            logger.debug("Filtering by exact last_activity date: %s", last_activity)
        if last_activity_after:
            queryset = queryset.filter(customerrelationship__last_activity__gte=last_activity_after)
            logger.debug("Filtering by last_activity_after: %s", last_activity_after)
        if last_activity_before:
            queryset = queryset.filter(customerrelationship__last_activity__lte=last_activity_before)
            logger.debug("Filtering by last_activity_before: %s", last_activity_before)

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
                    "customer_id": app_user.customer_id,
                    "phone_number": app_user.phone_number,
                    "created": app_user.created,
                    "birthday": app_user.birthday,
                    "last_updated": app_user.last_updated,
                    "address": {
                        "address_id": app_user.address.id,
                        "street": app_user.address.street,
                        "street_number": app_user.address.street_number,
                        "city_code": app_user.address.city_code,
                        "city": app_user.address.city,
                        "country": app_user.address.country,
                    },
                    "customer_relationships": [
                        {
                            "relationship_id": relationship.id,
                            "points": relationship.points,
                            "created": relationship.created,
                            "last_activity": relationship.last_activity,
                        }
                        for relationship in app_user.customerrelationship_set.all()
                    ],
                }
            )
    except Exception as e:
        logger.error("Error serializing data: %s", e)
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
