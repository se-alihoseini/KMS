from pydantic import BaseModel

class TestUserValidator(BaseModel):

    number: int
