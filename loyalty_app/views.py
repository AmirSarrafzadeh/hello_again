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
from django.utils.dateparse import parse_date
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
logger.setLevel(logging.INFO)

ALLOWED_PARAMETERS = {
    "page",
    "page_size",
    "sort_by",
    "order",
    "id",
    "first_name",
    "last_name",
    "gender",
    "customer_id",
    "phone_number",
    "appuser_created",
    "appuser_created_after",
    "appuser_created_before",
    "birthday",
    "last_updated",
    "last_updated_after",
    "last_updated_before",
    "address_id",
    "street",
    "street_number",
    "city_code",
    "city",
    "country",
    "relationship_id",
    "points",
    "relationship_created",
    "relationship_created_after",
    "relationship_created_before",
    "last_activity",
    "last_activity_after",
    "last_activity_before",
}


# Helper function to get all fields from a model
def get_model_fields(model):
    return [field.name for field in model._meta.get_fields()]


# Get all field names for sorting validation
appuser_fields = get_model_fields(AppUser)
address_fields = [f"address__{field}" for field in get_model_fields(Address)]
customerrelationship_fields = [f"customerrelationship__{field}" for field in get_model_fields(CustomerRelationship)]

# Combine all field names for validation
all_sortable_fields = appuser_fields + address_fields + customerrelationship_fields


def list_entries(request):
    """
    Lists entries from AppUser, Address, and CustomerRelationship.
    Includes filtering, sorting, and pagination with support for dynamic filters and date queries.
    """
    logger.info("Incoming request to entries endpoint with parameters: %s", request.GET.dict())

    # Validate query parameters
    unexpected_parameters = [param for param in request.GET if param not in ALLOWED_PARAMETERS]
    if unexpected_parameters:
        logger.error("Unexpected parameters: %s", unexpected_parameters)
        return JsonResponse(
            {"error": f"Invalid parameters: {', '.join(unexpected_parameters)}"}, status=400
        )

    try:
        # Extract filter and sort parameters
        filters = {key: value for key, value in request.GET.items() if
                   key not in ["sort_by", "order", "page", "page_size"]}
        sort_by = request.GET.get("sort_by", "id")
        order = request.GET.get("order", "asc")
        page = int(request.GET.get("page", 1))
        page_size = int(request.GET.get("page_size", 10))

        # Validate the sort field
        if sort_by not in all_sortable_fields:
            logger.error("Invalid sort_by field: %s", sort_by)
            return JsonResponse({"error": f"Invalid sort_by field: {sort_by}"}, status=400)

        logger.info("Parameters extracted successfully")
    except ValueError:
        logger.error("Invalid query parameters")
        return JsonResponse({"error": "Invalid query parameters"}, status=400)

    # Validate sort order
    if order == "desc":
        sort_by = f"-{sort_by}"

    # Build the base queryset
    queryset = AppUser.objects.select_related("address").prefetch_related("customerrelationship_set")

    logger.error("Queryset: %s", str(queryset.query))

    try:
        for field, value in filters.items():
            if field == "address_id":  # Specific handling for address_id
                queryset = queryset.filter(address__id=value)
                logger.debug("Filtering by Address ID: %s", value)
            elif hasattr(AppUser, field):  # Filter for AppUser fields
                queryset = queryset.filter(**{f"{field}__iexact": value})
                logger.debug("Filtering AppUser by %s: %s", field, value)
            elif hasattr(Address, field):  # Filter for Address fields
                queryset = queryset.filter(**{f"address__{field}__iexact": value})
                logger.debug("Filtering Address by %s: %s", field, value)
            elif field == "relationship_id":  # Specific handling for relationship_id
                queryset = queryset.filter(customerrelationship__id=value)  # Use related ForeignKey
                logger.debug("Filtering by Relationship ID: %s", value)
            elif hasattr(CustomerRelationship, field):  # Filter for CustomerRelationship fields
                queryset = queryset.filter(**{f"customerrelationship__{field}__iexact": value})
                logger.debug("Filtering CustomerRelationship by %s: %s", field, value)
    except Exception as e:
        logger.error("Error applying filters: %s", e)
        return JsonResponse({"error": "Error applying filters"}, status=400)

    try:
        # Filter by CustomerRelationship ID
        relationship_id = request.GET.get("relationship_id")
        if relationship_id:
            queryset = queryset.filter(customerrelationship__id=relationship_id)
            logger.debug("Filtering by CustomerRelationship ID: %s", relationship_id)

        # Separate filtering for AppUser's `created`
        appuser_created = request.GET.get("appuser_created")
        appuser_created_after = request.GET.get("appuser_created_after")
        appuser_created_before = request.GET.get("appuser_created_before")

        if appuser_created:
            appuser_created_date = parse_date(appuser_created)
            if appuser_created_date:
                queryset = queryset.filter(created__date=appuser_created_date)
                logger.debug("Filtering AppUser by exact created date: %s", appuser_created_date)
        if appuser_created_after:
            appuser_created_after_date = parse_date(appuser_created_after)
            if appuser_created_after_date:
                queryset = queryset.filter(created__date__gte=appuser_created_after_date)
                logger.debug("Filtering AppUser by created_after date: %s", appuser_created_after_date)
        if appuser_created_before:
            appuser_created_before_date = parse_date(appuser_created_before)
            if appuser_created_before_date:
                queryset = queryset.filter(created__date__lte=appuser_created_before_date)
                logger.debug("Filtering AppUser by created_before date: %s", appuser_created_before_date)

        # Separate filtering for CustomerRelationship's `created`
        relationship_created = request.GET.get("relationship_created")
        relationship_created_after = request.GET.get("relationship_created_after")
        relationship_created_before = request.GET.get("relationship_created_before")

        date_filters = {}
        if relationship_created:
            relationship_created_date = parse_date(relationship_created)
            if relationship_created_date:
                queryset = queryset.filter(customerrelationship__created__date=relationship_created_date)
                logger.debug("Filtering CustomerRelationship by exact created date: %s", relationship_created_date)
        if relationship_created_after:
            relationship_created_after_date = parse_date(relationship_created_after)
            if relationship_created_after_date:
                date_filters['customerrelationship__created__date__gte'] = relationship_created_after_date
                logger.debug("Filtering CustomerRelationship by created_after date: %s",
                             relationship_created_after_date)
        if relationship_created_before:
            relationship_created_before_date = parse_date(relationship_created_before)
            if relationship_created_before_date:
                date_filters['customerrelationship__created__date__lte'] = relationship_created_before_date
                logger.debug("Filtering CustomerRelationship by created_before date: %s",
                             relationship_created_before_date)

        # Similarly handle `last_updated` in `AppUser`
        last_updated = request.GET.get("last_updated")
        last_updated_after = request.GET.get("last_updated_after")
        last_updated_before = request.GET.get("last_updated_before")

        if last_updated:
            last_updated_date = parse_date(last_updated)
            if last_updated_date:
                queryset = queryset.filter(last_updated__date=last_updated_date)
                logger.debug("Filtering by exact last_updated date: %s", last_updated_date)
        if last_updated_after:
            last_updated_after_date = parse_date(last_updated_after)
            if last_updated_after_date:
                queryset = queryset.filter(last_updated__date__gte=last_updated_after_date)
                logger.debug("Filtering by last_updated_after date: %s", last_updated_after_date)
        if last_updated_before:
            last_updated_before_date = parse_date(last_updated_before)
            if last_updated_before_date:
                queryset = queryset.filter(last_updated__date__lte=last_updated_before_date)
                logger.debug("Filtering by last_updated_before date: %s", last_updated_before_date)

        # Handle `last_activity` in `CustomerRelationship`
        last_activity = request.GET.get("last_activity")
        last_activity_after = request.GET.get("last_activity_after")
        last_activity_before = request.GET.get("last_activity_before")

        if last_activity:
            last_activity_date = parse_date(last_activity)
            if last_activity_date:
                queryset = queryset.filter(customerrelationship__last_activity__date=last_activity_date)
                logger.debug("Filtering by exact last_activity date: %s", last_activity_date)

        if last_activity_after:
            last_activity_after_date = parse_date(last_activity_after)
            if last_activity_after_date:
                date_filters['customerrelationship__last_activity__date__gte'] = last_activity_after_date
                logger.debug("Filtering by last_activity_after date: %s", last_activity_after_date)
        if last_activity_before:
            last_activity_before_date = parse_date(last_activity_before)
            if last_activity_before_date:
                date_filters['customerrelationship__last_activity__date__lte'] = last_activity_before_date
                logger.debug("Filtering by last_activity_before date: %s", last_activity_before_date)

        queryset = queryset.filter(**date_filters)
    except Exception as e:
        logger.error("Error applying filters: %s", e)
        return JsonResponse({"error": "Error applying filters"}, status=400)

    try:
        # Apply sorting dynamically
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
