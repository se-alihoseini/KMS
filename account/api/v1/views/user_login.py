from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpRequest
from account.usecase import UserLoginUseCase
from utils.general_functions import get_request_body
from account.validators import UserLoginValidator


@require_http_methods(["POST"])
def user_login(request: HttpRequest) -> JsonResponse:
    user_data = get_request_body(request=request, validator=UserLoginValidator)
    use_case = UserLoginUseCase()
    data = use_case.execute(request_model=user_data)
    return data
