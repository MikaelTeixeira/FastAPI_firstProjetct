from pydantic import BaseModel
from typing import Optional

'''
Este arquivo equivale aos DTO's da aplicação.

No FASTAPI os DTOs são definidos usando o Pydantic.

Diferente do Spring não precisa criar mappers manuais nem camadas adicionais de validação. 
O Framework já faz a maior parte do trabalho usando a biblioteca Pydantic.
'''

class UserBase(BaseModel):
    name: str
    email: str
    age: int

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
    password: Optional[str] = None


class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    activate_user:bool

    class Config:
        from_attributes = True
