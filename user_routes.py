from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.models import User
from schemas import UserCreate, UserResponse, UserUpdate
from dependences import get_db
from rabbitmq_client import publish_message
from security import get_current_user
from services import UserService

user_router = APIRouter(tags=["Users"])


@user_router.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    service = UserService(db)
    created_user = service.create_user(user)
    publish_message(
        queue_name="ms1_user_events",
        event_type="user.created",
        payload={
            "user_id": created_user.id,
            "email": created_user.email,
        },
    )
    return created_user


@user_router.get("/users/", response_model=list[UserResponse])
def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = UserService(db)

    return service.get_users()


@user_router.get("/users/{user_id}", response_model=UserResponse)
def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = UserService(db)

    return service.get_user_by_id(user_id)


@user_router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = UserService(db)
    result = service.delete_user(user_id)
    publish_message(
        queue_name="ms1_user_events",
        event_type="user.deleted",
        payload={
            "user_id": user_id,
            "deleted_by": current_user.email,
        },
    )
    return result



@user_router.put("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = UserService(db)
    updated_user = service.update_user(user_id, user_data)
    publish_message(
        queue_name="ms1_user_events",
        event_type="user.updated",
        payload={
            "user_id": updated_user.id,
            "updated_by": current_user.email,
        },
    )
    return updated_user
