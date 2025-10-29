from account.models import User
from django.db import IntegrityError


class UserRepository:

    @staticmethod
    def get_or_create_user(email: str, password: str) -> User:
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "username": email,
            }
        )
        if created:
            user.set_password(password)
            user.save()
        return user
