from backbone.interface import UseCaseInterface
from django.http import JsonResponse
from account.validators.user_register_validator import UserRegisterValidator
from account.repository import UserRepository

class UserRegisterUseCase(UseCaseInterface):
    def process_request(self, payload: UserRegisterValidator):
        try:
            user = UserRepository.get_or_create_user(
                email=payload.email,
                password=payload.password
            )

            return JsonResponse(
                {
                    "success": True,
                    "message": f"User {user.username} registered successfully",
                },
                status=201,
            )

        except Exception as e:
            return JsonResponse(
                {
                    "success": False,
                    "message": f"Failed to register user: {str(e)}",
                },
                status=400,
            )
