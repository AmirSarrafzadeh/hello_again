"""
Author: Amir Sarrafzadeh Arasi
Date: 2024-12-21

Description:
This script defines a RESTful API for a loyalty application, built using the Django Ninja framework.
It includes endpoints for retrieving paginated and filtered lists of users (`AppUser`) with their
associated addresses and customer relationships, along with a simple test endpoint.
"""

from ninja import NinjaAPI, Schema
from django.http import JsonResponse
from django.core.paginator import Paginator
from loyalty_app.models import AppUser, Address, CustomerRelationship
from typing import List, Optional

# Initialize the NinjaAPI
api = NinjaAPI(
    title="Hello Again API",
    version="1.0.0",
    description=(
        "This API for Hello Again project Loyalty App"
    ),
)


# Define request and response schemas
class AddressSchema(Schema):
    street: str
    street_number: str
    city_code: str
    city: str
    country: str


class CustomerRelationshipSchema(Schema):
    points: int
    created: str
    last_activity: str


class AppUserSchema(Schema):
    id: int
    first_name: str
    last_name: str
    gender: Optional[str]
    phone_number: Optional[str]
    address: AddressSchema
    customer_relationships: List[CustomerRelationshipSchema]


class PaginatedResponse(Schema):
    page: int
    total_pages: int
    total_items: int
    results: List[AppUserSchema]


# Define the endpoint with NinjaAPI
@api.get("/entries", response=PaginatedResponse, tags=["Entries"])
def list_entries(
        request,
        page: int = 1,
        page_size: int = 10,
        sort_by: str = "id",
        order: str = "asc",
        **filters,
):
    """
    ### Description
    This endpoint retrieves a list of `AppUser` entries with related `Address` and `CustomerRelationship` data.
    It supports:
    - Dynamic filtering on fields across `AppUser`, `Address`, and `CustomerRelationship` models.
    - Sorting by any valid field using the `sort_by` parameter.
    - Pagination with `page` and `page_size` parameters.

    ### Query Parameters
    - `page` (int): Page number for pagination (default: 1).
    - `page_size` (int): Number of items per page (default: 10).
    - `sort_by` (str): Field to sort by (default: `id`).
    - `order` (str): Sort order, either `asc` or `desc` (default: `asc`).
    - Additional filter parameters are dynamically matched to fields in the models.

    ### Example Query
    ```
    /entries?page=1&page_size=5&sort_by=first_name&order=asc&gender=F&city=Taylorburgh
    ```

    ### Example Response
    ```json
    {
        "page": 1,
        "total_pages": 2,
        "total_items": 12,
        "results": [
            {
                "id": 1,
                "first_name": "Cynthia",
                "last_name": "Wallace",
                "gender": "O",
                "phone_number": "743-698-5427x65",
                "address": {
                    "street": "Stanley Manors",
                    "street_number": "46852",
                    "city_code": "21040",
                    "city": "Russellmouth",
                    "country": "Lesotho"
                },
                "customer_relationships": [
                    {
                        "points": 2663219,
                        "created": "2024-12-20T18:28:21.124837+01:00",
                        "last_activity": "2024-02-18T22:33:47+01:00"
                    }
                ]
            }
        ]
    }
    ```
    """
    try:
        # Validate sort order
        if order == "desc":
            sort_by = f"-{sort_by}"

        # Build the base queryset
        queryset = AppUser.objects.select_related("address").prefetch_related(
            "customerrelationship_set"
        )

        # Apply filtering dynamically with case-insensitive exact match
        for field, value in filters.items():
            if hasattr(AppUser, field):
                queryset = queryset.filter(**{f"{field}__iexact": value})
            elif hasattr(Address, field):
                queryset = queryset.filter(**{f"address__{field}__iexact": value})
            elif hasattr(CustomerRelationship, field):
                queryset = queryset.filter(**{f"customerrelationship__{field}__iexact": value})

        # Apply sorting
        queryset = queryset.order_by(sort_by)

        # Paginate results
        paginator = Paginator(queryset, page_size)
        paginated_data = paginator.get_page(page)

        # Serialize data
        results = []
        for app_user in paginated_data:
            results.append(
                AppUserSchema(
                    id=app_user.id,
                    first_name=app_user.first_name,
                    last_name=app_user.last_name,
                    gender=app_user.gender,
                    phone_number=app_user.phone_number,
                    address=AddressSchema(
                        street=app_user.address.street,
                        street_number=app_user.address.street_number,
                        city_code=app_user.address.city_code,
                        city=app_user.address.city,
                        country=app_user.address.country,
                    ),
                    customer_relationships=[
                        CustomerRelationshipSchema(
                            points=relationship.points,
                            created=str(relationship.created),
                            last_activity=str(relationship.last_activity),
                        )
                        for relationship in app_user.customerrelationship_set.all()
                    ],
                )
            )

        return {
            "page": page,
            "total_pages": paginator.num_pages,
            "total_items": paginator.count,
            "results": results,
        }
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


# Example additional endpoint for testing
@api.get("/test", tags=["Test"])
def test_api(request):
    """
    Endpoint to verify the API is operational.

    Returns:
        dict: A success message indicating the API is functioning properly.
    """
    return {"status": "success", "message": "Loyalty app api is operational."}