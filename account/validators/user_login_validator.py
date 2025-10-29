from pydantic import BaseModel

class UserLoginValidator(BaseModel):
    email: str
    password: str
