from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependences import get_db
from rabbitmq_client import publish_message
from rate_limit import limit_requests
from schemas import BookCreate, BookResponse, BookUpdate
from security import get_current_library_user
from services import BookService

book_router = APIRouter(prefix="/books", tags=["Books"])


@book_router.post(
    "/",
    response_model=BookResponse,
    dependencies=[Depends(limit_requests("ms2-books-create", 10, 60))],
)
def create_book(
    book: BookCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_library_user),
):
    service = BookService(db)
    created_book = service.create_book(book)
    publish_message(
        queue_name="ms2_book_events",
        event_type="book.created",
        payload={
            "book_id": created_book.id,
            "isbn": created_book.isbn,
            "owner_user_id": created_book.owner_user_id,
        },
    )
    return created_book


@book_router.get(
    "/",
    response_model=list[BookResponse],
    dependencies=[Depends(limit_requests("ms2-books-list", 30, 60))],
)
def list_books(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_library_user),
):
    service = BookService(db)
    return service.get_books()


@book_router.get(
    "/{book_id}",
    response_model=BookResponse,
    dependencies=[Depends(limit_requests("ms2-books-detail", 30, 60))],
)
def get_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_library_user),
):
    service = BookService(db)
    return service.get_book_by_id(book_id)


@book_router.put(
    "/{book_id}",
    response_model=BookResponse,
    dependencies=[Depends(limit_requests("ms2-books-update", 15, 60))],
)
def update_book(
    book_id: int,
    book_data: BookUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_library_user),
):
    service = BookService(db)
    updated_book = service.update_book(book_id, book_data)
    publish_message(
        queue_name="ms2_book_events",
        event_type="book.updated",
        payload={
            "book_id": updated_book.id,
            "isbn": updated_book.isbn,
            "owner_user_id": updated_book.owner_user_id,
        },
    )
    return updated_book


@book_router.delete(
    "/{book_id}",
    dependencies=[Depends(limit_requests("ms2-books-delete", 10, 60))],
)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_library_user),
):
    service = BookService(db)
    result = service.delete_book(book_id)
    publish_message(
        queue_name="ms2_book_events",
        event_type="book.deleted",
        payload={"book_id": book_id},
    )
    return result
