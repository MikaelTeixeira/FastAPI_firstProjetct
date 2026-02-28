from pydantic import BaseModel

class UserBase(BaseModel):
    password: str
    email: str
    idade: int

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        from_atrbibutes = True