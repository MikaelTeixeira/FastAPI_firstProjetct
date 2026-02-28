from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate, UserResponse
from dependences import get_db
from passlib.context import CryptContext

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password:str):
    return pwd_context.hash(password)


@router.post("/users/", response_model=UserResponse)
def create_user(user:UserCreate, db:Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == user.email).first()

    if db_user:
        raise HTTPException(
            status_code = 400,
            detail="Email already registered"
        )
    new_user = User(
        name=user.name,
        email=user.email,
        age=user.age,
        hashed_password=hash_password(user.password)
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return new_user


@router.get("/users", response_model = list[UserResponse])
def list_users(db:Session=Depends(get_db)):

    users = db.query(User).all()

    return users    

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id:int,db:Session=Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code = 404,
            detail = "User not found"
        )         
    
    return user

@router.delete("/users/{user_id}")
def delete_user(user_id:int, db:Session=Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code = 404,
            detail = "User not found"
        )
    
    db.delete(user)
    db.commit()

    return {"detail": "User was sucessfully deleted"}



