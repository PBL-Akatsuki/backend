from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str
    password: str

    class config:
        form_attributes = True 

class CreateUser(UserBase):
    class config:
        form_attributes = True
