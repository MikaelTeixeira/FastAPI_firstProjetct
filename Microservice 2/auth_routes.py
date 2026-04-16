from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from dependences import get_db
from rabbitmq_client import publish_message
from rate_limit import limit_requests
from schemas import LibraryUserResponse, Token
from security import create_access_token, get_current_library_user
from services import LibraryUserService

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post(
    "/login",
    response_model=Token,
    dependencies=[Depends(limit_requests("ms2-login", 5, 60))],
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    service = LibraryUserService(db)
    user = service.authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.email})
    publish_message(
        queue_name="ms2_book_events",
        event_type="library_user.login",
        payload={"library_user_id": user.id, "email": user.email},
    )
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.get("/me", response_model=LibraryUserResponse)
def read_current_user(current_user=Depends(get_current_library_user)):
    return current_user
