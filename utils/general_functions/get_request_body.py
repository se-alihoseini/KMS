import json
from django.http import HttpRequest
from pydantic import BaseModel, ValidationError

def get_request_body(request: HttpRequest, validator: type[BaseModel]) -> BaseModel:
    if not request.body:
        raise ValueError("Request body is empty")

    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON body: {e}")

    try:
        validated_obj = validator(**data)
    except ValidationError as e:
        raise ValueError(f"Validation error: {e}")

    return validated_obj
