from typing import Any

from django.utils.decorators import method_decorator

from drf_yasg.utils import swagger_auto_schema

from rest_framework import status

VIEWSET_METHODS = ("list", "retrieve", "create", "update", "partial_update", "destroy")


def viewset_swagger(additional_name: str,
                    method_names: tuple[str, ...] = VIEWSET_METHODS,
                    additional_data: dict[str, Any] = None):
    """For swagger operation_id change and creation status codes in some methods"""

    def decorator(cls):
        if not hasattr(cls, "_decorators_applied"):
            for method_name in method_names:
                additional_method_data = {"responses": {}}

                if method_name == "destroy":
                    additional_method_data["responses"][status.HTTP_204_NO_CONTENT] = "Destroyed successfully"
                if method_name in ["create", "update", "partial_update"]:
                    additional_method_data["responses"][status.HTTP_400_BAD_REQUEST] = "Some fields are invalid"
                if method_name in ["retrieve", "update", "partial_update", "destroy"]:
                    additional_method_data["responses"][status.HTTP_404_NOT_FOUND] = "Not found obj by id"
                if additional_data is not None and method_name in additional_data.keys():
                    if "responses" in additional_data[method_name]:
                        additional_method_data["responses"].update(additional_data[method_name].pop("responses"))
                    additional_method_data.update(additional_data[method_name])

                original_method = getattr(cls, method_name)
                decorated_method = method_decorator(
                    swagger_auto_schema(operation_id=f"{additional_name} {method_name}", **additional_method_data)
                )(original_method)
                setattr(cls, method_name, decorated_method)
            cls.decorators_applied = True
        return cls

    return decorator
