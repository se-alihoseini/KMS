from functools import wraps
from django.http import JsonResponse


def admin_permission():
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            user = request.user
            if not user.groups.filter(name="admin").exists():
                return JsonResponse({"success": False, "message": "Permission denied"}, status=403)

            return func(request, *args, **kwargs)
        return wrapper
    return decorator
