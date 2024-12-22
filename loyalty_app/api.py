"""
Author: Amir Sarrafzadeh Arasi
Date: 2024-12-21

Description:
This script defines a RESTful API for a loyalty application, built using the Django Ninja framework.
It includes endpoints for retrieving paginated and filtered lists of users (`AppUser`) with their
associated addresses and customer relationships, along with a simple test endpoint.
"""
from datetime import date, datetime
from ninja import NinjaAPI, Schema, Query
from typing import List, Optional


# Define request and response schemas
class AddressSchema(Schema):
    id: int
    street: str
    street_number: str
    city_code: str
    city: str
    country: str


class CustomerRelationshipSchema(Schema):
    id: int
    points: int
    created: datetime
    last_activity: datetime
    appuser_id: int


class AppUserSchema(Schema):
    id: int
    first_name: str
    last_name: str
    gender: str
    customer_id: str
    phone_number: str
    created: datetime
    birthday: date
    last_updated: datetime
    address: List[AddressSchema]
    customerrelationship: List[CustomerRelationshipSchema]


class PaginatedResponse(Schema):
    page: int
    total_pages: int
    total_items: int
    results: List[AppUserSchema]


# Initialize the NinjaAPI
api = NinjaAPI(
    title="Hello Again API",
    version="1.0.0",
    description=(
        "This API for Hello Again project Loyalty App"
    )
)


# Define the endpoint with NinjaAPI
@api.get("/entries", response=PaginatedResponse, tags=["Entries"])
def list_entries(
        request,
        page: int = Query(1),
        page_size: int = Query(10),
        sort_by: str = Query("id", description="Field to sort by, check the API documentation for valid fields"),
        order: str = Query("asc", description="Sort order, either `asc` or `desc`"),
        id: Optional[int] = Query(None, description="Filter by AppUser ID , Sample value: 1"),
        first_name: Optional[str] = Query(None, description="Filter by AppUser first name, Sample value: John"),
        last_name: Optional[str] = Query(None, description="Filter by AppUser last name, Sample value: Brown"),
        gender: Optional[str] = Query(None, description="Filter by gender, Values: [Male, Female, Other]"),
        customer_id: Optional[str] = Query(None,
                                           description="Filter by customer ID, Sample value: 91bf0d4e-f853-46b1-a8aa-6aa6ef6b43df"),
        phone_number: Optional[str] = Query(None,
                                            description="Filter by phone number, Sample value: 001-446-868-0060x376"),
        appuser_created: Optional[str] = Query(None,
                                               description="Filter by exact created date, Sample value: 2017-12-21"),
        appuser_created_after: Optional[str] = Query(None,
                                                     description="Filter by created date after a specific date, Sample value: 2013-07-22"),
        appuser_created_before: Optional[str] = Query(None,
                                                      description="Filter by created date before a specific date, Sample value: 2019-12-21"),
        birthday: Optional[str] = Query(None, description="Filter by birthday, Sample value: 1990-12-21"),
        last_updated: Optional[str] = Query(None,
                                            description="Filter by exact last updated date, Sample value: 2024-11-03"),
        last_updated_after: Optional[str] = Query(None,
                                                  description="Filter by last updated date after a specific date, Sample value: 2024-04-12"),
        last_updated_before: Optional[str] = Query(None,
                                                   description="Filter by last updated date before a specific date, Sample value: 2024-03-23"),
        address_id: Optional[int] = Query(None, description="Filter by Address ID, Sample value: 43"),
        street: Optional[str] = Query(None, description="Filter by street name, Sample value: Mary Burg"),
        street_number: Optional[str] = Query(None, description="Filter by street number, Sample value: 05043"),
        city_code: Optional[str] = Query(None, description="Filter by city code, Sample value: 34487"),
        city: Optional[str] = Query(None, description="Filter by city name, Sample value: Port Brian"),
        country: Optional[str] = Query(None, description="Filter by country name, Sample value: Denmark"),
        relationship_id: Optional[int] = Query(None, description="Filter by CustomerRelationship ID, Sample value: 93"),
        points: Optional[int] = Query(None, description="Filter by points, Sample value: 223"),
        relationship_created: Optional[str] = Query(None,
                                                    description="Filter by exact created date, Sample value: 2017-10-02"),
        relationship_created_after: Optional[str] = Query(None,
                                                          description="Filter by created date after a specific date, Sample value: 2013-07-22"),
        relationship_created_before: Optional[str] = Query(None,
                                                           description="Filter by created date before a specific date, Sample value: 2019-12-21"),
        last_activity: Optional[str] = Query(None,
                                             description="Filter by exact last activity date, Sample value: 2024-11-03"),
        last_activity_after: Optional[str] = Query(None,
                                                   description="Filter by last activity date after a specific date, Sample value: 2024-04-12"),
        last_activity_before: Optional[str] = Query(None,
                                                    description="Filter by last activity date before a specific date, Sample value: 2024-03-23"),
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

    ### Sorting Fields
    - `id`, `first_name`, `last_name`, `gender`, `customer_id`, `phone_number`, `created`, `birthday`, `last_updated`

    - `address__id`, `address__street`, `address__street_number`, `address__city_code`, `address__city`, `address__country`

    - `customerrelationship__id`, `customerrelationship__points`, `customerrelationship__created`, `customerrelationship__last_activity`

    ### Example Query
    ```
    /entries?page=1&page_size=5&sort_by=first_name&order=asc&gender=F&city=Taylorburgh
    ```

    ### Example Response
    ```json
  {
      "page": 1,
      "total_pages": 1,
      "total_items": 1,
      "results": [
        {
          "id": 59,
          "first_name": "Ian",
          "last_name": "Warren",
          "gender": "Female",
          "customer_id": "b418bf7c-7fff-4a41-bd2c-2b6f58eeda00",
          "phone_number": "315.433.2160",
          "created": "2015-08-25T00:00:00Z",
          "birthday": "1960-12-23",
          "last_updated": "2024-06-25T14:38:33Z",
          "address": {
            "address_id": 96,
            "street": "Smith Forks",
            "street_number": "27455",
            "city_code": "34557",
            "city": "Charlesport",
            "country": "Malta"
          },
          "customer_relationships": [
            {
              "relationship_id": 22,
              "points": 27,
              "created": "2014-03-23T00:00:00Z",
              "last_activity": "2024-01-13T08:03:37Z"
            },
            {
              "relationship_id": 214,
              "points": 138,
              "created": "2014-08-26T00:00:00Z",
              "last_activity": "2024-01-01T20:49:18Z"
            }
          ]
        }
      ]
  }
    ```
    """

# Example additional endpoint for testing
@api.get("/test", tags=["Test API"])
def test_api(request):
    """
    Endpoint to verify the API is operational.

    Returns:
        dict: A success message indicating the API is functioning properly.
    """
    return {"status": "success", "message": "Loyalty app api is operational."}
