from functools import wraps
from django.http import JsonResponse

def check_group_assignment(model_name: str):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            user = request.user
            obj = kwargs.get("obj")
            if not obj:
                return JsonResponse({"success": False, "message": "Object not provided"}, status=400)

            user_group_ids = user.groups.values_list("id", flat=True)

            if model_name == "article":
                obj_group_ids = obj.groups.values_list("id", flat=True)
            elif model_name == "knowledge":
                obj_group_ids = obj.article.all().values_list("groups__id", flat=True)
            else:
                return JsonResponse({"success": False, "message": "Invalid model_name"}, status=400)

            if not set(user_group_ids).intersection(set(obj_group_ids)):
                return JsonResponse({"success": False, "message": "User is not assigned to any group of this object"}, status=403)

            return func(request, *args, **kwargs)
        return wrapper
    return decorator
