from pydantic import BaseModel
from account.models import User

class TestUserValidator(BaseModel):
    user: User
    number: int


    class Config:
        arbitrary_types_allowed = True
