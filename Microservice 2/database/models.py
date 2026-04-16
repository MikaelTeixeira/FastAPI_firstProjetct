from sqlalchemy import Boolean, Column, Integer, String

from .db_setup import Base


class LibraryUser(Base):
    __tablename__ = "library_users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    isbn = Column(String, unique=True, index=True, nullable=False)
    publication_year = Column(Integer, nullable=False)
    genre = Column(String, nullable=False)
    available_copies = Column(Integer, nullable=False, default=1)
    owner_user_id = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
