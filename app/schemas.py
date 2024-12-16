from pydantic import BaseModel, EmailStr, ConfigDict

class UserBase(BaseModel):
    username: str
    email: EmailStr  # Ensures email validation
    password: str

    model_config = ConfigDict(
        from_attributes=True,  # Replaces 'orm_mode' for SQLAlchemy integration
        populate_by_name=True  # Allow using aliases to populate the fields
    )


class CreateUser(UserBase):
    pass  # Inherits all fields and configurations from UserBase


class LoginUser(BaseModel):
    username_or_email: str  # Either username or email for login
    password: str  # Password for authentication

    model_config = ConfigDict(
        from_attributes=False,
        populate_by_name=True
    )
