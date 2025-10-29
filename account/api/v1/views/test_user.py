from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpRequest
from account.usecase import TestUserUseCase
from utils.general_functions import get_request_body
from account.validators import TestUserValidator



@require_http_methods(["GET"])
def test_user(request: HttpRequest) -> JsonResponse:

    # user_data = get_request_body(request) => necessary for POST requests
    number = request.GET.get('number', 10)
    user_data = TestUserValidator(number=number)

    use_case = TestUserUseCase()
    data = use_case.execute(request_model=user_data)
    return data
