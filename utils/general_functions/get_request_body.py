import orjson as json
from django.http import HttpRequest


def get_request_body(request: HttpRequest) -> dict:
    if request.body:
        try:
            request_data = json.loads(request.body.decode("utf-8"))
        except json.JSONDecodeError:
            request_data = {}
    else:
        request_data = {}
    return request_data
