from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    email: str
    username: str
    hashed_password: str
    auth_provider: str = "local"

class Token(BaseModel):
    access_token: str
    token_type: str