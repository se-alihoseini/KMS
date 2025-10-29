import jwt
from zoneinfo import ZoneInfo

from datetime import datetime, timedelta
from django.conf import settings
from account.models import User

JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120
REFRESH_TOKEN_EXPIRE_DAYS = 7
tehran_tz = ZoneInfo("Asia/Tehran")



def create_jwt_tokens(user: User) -> dict:
    now = datetime.now(tz=tehran_tz)

    access_payload = {
        "user_id": user.id,
        "username": user.username,
        "exp": now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        "type": "access",
    }

    refresh_payload = {
        "user_id": user.id,
        "exp": now + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        "type": "refresh",
    }

    access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm=JWT_ALGORITHM)
    refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm=JWT_ALGORITHM)

    return {
        "access": access_token,
        "refresh": refresh_token,
    }
