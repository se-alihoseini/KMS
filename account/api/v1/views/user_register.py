from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpRequest
from account.usecase.user_register_usecase import UserRegisterUseCase
from utils.general_functions.get_request_body import get_request_body
from account.validators.user_register_validator import UserRegisterValidator

@require_http_methods(["POST"])
def user_register(request: HttpRequest) -> JsonResponse:
    payload = get_request_body(request=request, validator=UserRegisterValidator)
    use_case = UserRegisterUseCase()
    data = use_case.execute(request_model=payload)
    return data
