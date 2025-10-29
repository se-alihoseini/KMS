from functools import wraps
from django.http import JsonResponse
from account.models import User
import jwt
from django.conf import settings

JWT_ALGORITHM = "HS256"


def login_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JsonResponse({"success": False, "message": "Authorization token required"}, status=401)

        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[JWT_ALGORITHM])
            user_id = payload.get("user_id")
            user = User.objects.get(id=user_id)
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
            return JsonResponse({"success": False, "message": "Invalid or expired token"}, status=401)

        request.user = user
        return func(request, *args, **kwargs)

    return wrapper
