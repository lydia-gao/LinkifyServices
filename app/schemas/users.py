from pydantic import BaseModel


class UserVerification(BaseModel):
    password: str
    new_password: str
