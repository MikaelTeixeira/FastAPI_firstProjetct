from fastapi import HTTPException
from sqlalchemy.orm import Session

from database.models import Book, LibraryUser
from schemas import BookCreate, BookUpdate, LibraryUserCreate, LibraryUserUpdate
from security import hash_password, verify_password


class LibraryUserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: LibraryUserCreate):
        existing_user = (
            self.db.query(LibraryUser).filter(LibraryUser.email == user.email).first()
        )

        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        new_user = LibraryUser(
            name=user.name,
            email=user.email,
            hashed_password=hash_password(user.password),
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def get_users(self):
        return self.db.query(LibraryUser).filter(LibraryUser.is_active == True).all()

    def authenticate_user(self, email: str, password: str):
        user = (
            self.db.query(LibraryUser)
            .filter(LibraryUser.email == email, LibraryUser.is_active == True)
            .first()
        )

        if not user or not verify_password(password, user.hashed_password):
            return None

        return user

    def update_user(self, user_id: int, user_data: LibraryUserUpdate):
        user = (
            self.db.query(LibraryUser)
            .filter(LibraryUser.id == user_id, LibraryUser.is_active == True)
            .first()
        )

        if not user:
            raise HTTPException(status_code=404, detail="Library user not found")

        if user_data.name is not None:
            user.name = user_data.name

        if user_data.email is not None:
            user.email = user_data.email

        if user_data.password is not None:
            user.hashed_password = hash_password(user_data.password)

        self.db.commit()
        self.db.refresh(user)
        return user


class BookService:
    def __init__(self, db: Session):
        self.db = db

    def create_book(self, book: BookCreate):
        existing_book = self.db.query(Book).filter(Book.isbn == book.isbn).first()

        if existing_book:
            raise HTTPException(status_code=400, detail="ISBN already registered")

        new_book = Book(
            title=book.title,
            author=book.author,
            isbn=book.isbn,
            publication_year=book.publication_year,
            genre=book.genre,
            available_copies=book.available_copies,
            owner_user_id=book.owner_user_id,
        )
        self.db.add(new_book)
        self.db.commit()
        self.db.refresh(new_book)
        return new_book

    def get_books(self):
        return self.db.query(Book).filter(Book.is_active == True).all()

    def get_book_by_id(self, book_id: int):
        book = (
            self.db.query(Book)
            .filter(Book.id == book_id, Book.is_active == True)
            .first()
        )

        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        return book

    def update_book(self, book_id: int, book_data: BookUpdate):
        book = (
            self.db.query(Book)
            .filter(Book.id == book_id, Book.is_active == True)
            .first()
        )

        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        update_data = book_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(book, field, value)

        self.db.commit()
        self.db.refresh(book)
        return book

    def delete_book(self, book_id: int):
        book = (
            self.db.query(Book)
            .filter(Book.id == book_id, Book.is_active == True)
            .first()
        )

        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        book.is_active = False
        self.db.commit()
        return {"detail": "Book deleted successfully"}

    def deactivate_books_by_owner(self, owner_user_id: int):
        books = (
            self.db.query(Book)
            .filter(Book.owner_user_id == owner_user_id, Book.is_active == True)
            .all()
        )

        for book in books:
            book.is_active = False

        self.db.commit()
        return len(books)
