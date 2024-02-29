from drf_yasg import openapi

from rest_framework import status


AUTH_TOKEN_SCHEMA = openapi.Parameter(
    name="Authorization",
    in_=openapi.IN_HEADER,
    type=openapi.TYPE_STRING,
    description="Bearer token for authentication",
    required=True,
    example="Bearer 5aa7eb4403faa4bca8048c4781831cdce2c11337",
    allow_empty_value=True,
)
user_doc = {
    "list": {
        "operation_description": "Returns all User model objects. Filtered by user.company.id from auth token.",
        "manual_parameters": [AUTH_TOKEN_SCHEMA],
        "responses": {
            status.HTTP_401_UNAUTHORIZED: "Unauthorized",
            status.HTTP_403_FORBIDDEN: "Forbidden",
        }
    },
    "create": {
        "operation_description": "Create user model object and userprofile model object for it",
        "manual_parameters": [AUTH_TOKEN_SCHEMA],

    },
    "retrieve": {
        "operation_description": "Return user model object by id",
        "manual_parameters": [AUTH_TOKEN_SCHEMA],
        "responses": {
            status.HTTP_401_UNAUTHORIZED: "Unauthorized",
            status.HTTP_403_FORBIDDEN: "Forbidden",
        },
    },
    "update": {
        "operation_description": "Full change user model object by id",
        "manual_parameters": [AUTH_TOKEN_SCHEMA],
        "responses": {
            status.HTTP_401_UNAUTHORIZED: "Unauthorized",
            status.HTTP_403_FORBIDDEN: "Forbidden",
        },
    },
    "partial_update": {
        "operation_description": "Partial change user model object by id",
        "manual_parameters": [AUTH_TOKEN_SCHEMA],
        "responses": {
            status.HTTP_401_UNAUTHORIZED: "Unauthorized",
            status.HTTP_403_FORBIDDEN: "Forbidden",
        },
    },
    "destroy": {
        "operation_description": "Destroy user model object by id",
        "manual_parameters": [AUTH_TOKEN_SCHEMA],
        "responses": {status.HTTP_401_UNAUTHORIZED: "Unauthorized", status.HTTP_403_FORBIDDEN: "Forbidden"},
    },
}
