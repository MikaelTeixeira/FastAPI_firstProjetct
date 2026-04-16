from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependences import get_db
from rate_limit import limit_requests
from schemas import LibraryUserCreate, LibraryUserResponse, LibraryUserUpdate
from security import get_current_library_user
from services import LibraryUserService

library_user_router = APIRouter(prefix="/library-users", tags=["Library Users"])


@library_user_router.post(
    "/",
    response_model=LibraryUserResponse,
    dependencies=[Depends(limit_requests("ms2-library-users-create", 10, 60))],
)
def create_library_user(user: LibraryUserCreate, db: Session = Depends(get_db)):
    service = LibraryUserService(db)
    return service.create_user(user)


@library_user_router.get(
    "/",
    response_model=list[LibraryUserResponse],
    dependencies=[Depends(limit_requests("ms2-library-users-list", 30, 60))],
)
def list_library_users(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_library_user),
):
    service = LibraryUserService(db)
    return service.get_users()


@library_user_router.put(
    "/{user_id}",
    response_model=LibraryUserResponse,
    dependencies=[Depends(limit_requests("ms2-library-users-update", 15, 60))],
)
def update_library_user(
    user_id: int,
    user_data: LibraryUserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_library_user),
):
    service = LibraryUserService(db)
    return service.update_user(user_id, user_data)
