from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.models import User
from schemas import UserCreate, UserResponse, UserUpdate
from dependences import get_db
from passlib.context import CryptContext
from services import UserService

user_router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password:str):
    
    return pwd_context.hash(password)


@user_router.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    service = UserService(db)

    return service.create_user(user)


@user_router.get("/users/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):

    service = UserService(db)

    return service.get_users()


@user_router.get("/users/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):

    service = UserService(db)

    return service.get_user_by_id(user_id)
@user_router.delete("/users/{user_id}")
def delete_user(user_id:int, db:Session=Depends(get_db)):

    user = db.query(User).filter(User.id == user_id, User.activate_user==True).first()

    if not user:
        raise HTTPException(
            status_code = 404,
            detail = "User not found"
        )
    
    user.activate_user = False
    db.commit()
    db.refresh(user)

    return {"detail": "User was sucessfully deleted"}



@user_router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id, User.activate_user==True).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    update_data = user_data.model_dump(exclude_unset=True)

    print("ANTES:", user.name)

    for field, value in update_data.items():
        if field == "password":
            user.hashed_password = hash_password(value)
        else:
            setattr(user, field, value)

    print("DEPOIS:", user.name)

    db.commit()
    db.refresh(user)

    return user