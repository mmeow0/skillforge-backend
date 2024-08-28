from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenRefresh(BaseModel):
    refresh_token: str

class UserLogin(BaseModel):
    email: str
    password: str