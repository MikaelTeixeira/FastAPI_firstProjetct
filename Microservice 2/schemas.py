from typing import Optional

from pydantic import BaseModel


class LibraryUserBase(BaseModel):
    name: str
    email: str


class LibraryUserCreate(LibraryUserBase):
    password: str


class LibraryUserResponse(LibraryUserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True


class LibraryUserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class BookBase(BaseModel):
    title: str
    author: str
    isbn: str
    publication_year: int
    genre: str
    available_copies: int
    owner_user_id: int


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None
    publication_year: Optional[int] = None
    genre: Optional[str] = None
    available_copies: Optional[int] = None
    owner_user_id: Optional[int] = None


class BookResponse(BookBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
