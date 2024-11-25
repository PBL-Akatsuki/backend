from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str
    password: str

    class Config:
        form_attributes = True 

class CreateUser(UserBase):
    class Config:
        form_attributes = True
