from pydantic import BaseModel

class UserRegisterValidator(BaseModel):
    email: str
    password: str
