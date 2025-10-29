from backbone.interface import UseCaseInterface
from django.contrib.auth import authenticate
from django.http import JsonResponse
from account.validators import UserLoginValidator
from utils.general_functions.jwt import create_jwt_tokens

class UserLoginUseCase(UseCaseInterface):
    def process_request(self, payload: UserLoginValidator):
        user = authenticate(username=payload.email, password=payload.password)
        if user is not None:
            tokens = create_jwt_tokens(user)
            return JsonResponse(
                {
                    "success": True,
                    "message": f"Welcome {user.username}",
                    "tokens": tokens,
                },
                status=200,
            )
        else:
            return JsonResponse(
                {"success": False, "message": "Invalid email or password"},
                status=401,
            )
