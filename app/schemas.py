from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr  # Ensures email validation
    password: str

    class Config:
        form_attributes = True


class CreateUser(UserBase):
    class Config:
        form_attributes = True


class LoginUser(BaseModel):
    username_or_email: str  # Either username or email
    password: str  # Password for authentication

    class Config:
        form_attributes = True
