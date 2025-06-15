# app/models/token.py
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: int | None = None  # user id (subject)
    exp: int | None = None  # expiration timestamp (unix)
