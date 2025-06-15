# app/models/user.py

from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str  # Required only at creation

class User(UserBase):
    id: Optional[int]

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str
