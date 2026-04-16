from sqlalchemy.orm import Session
from fastapi import HTTPException
from database.models import User
from schemas import UserCreate
from security import hash_password, verify_password


class UserService:

    def __init__(self, db= Session):

        self.db = db

    def create_user(self, user: UserCreate):

        db_user = self.db.query(User).filter(User.email == user.email).first()

        if db_user:
            raise HTTPException(
                status_code = 400,
                detail="Email alredy registered"
            )
        
        new_user = User(
            name=user.name,
            email=user.email,
            age=user.age,
            hashed_password=hash_password(user.password)
        )

        self.db.add(new_user)
        self.db.commit()

        self.db.refresh(new_user)

        return new_user

    def authenticate_user(self, email: str, password: str):
        user = (
            self.db.query(User)
            .filter(User.email == email, User.activate_user == True)
            .first()
        )

        if not user or not verify_password(password, user.hashed_password):
            return None

        return user
    
    def get_users(self):

        users = self.db.query(User).filter(User.activate_user==True).all()

        return users

    def get_user_by_id(self, user_id:int):

        user = self.db.query(User).filter(User.id == user_id, User.activate_user == True).first()

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        return user
    
    def update_user(self, user_id: int, user_data):
        user = self.db.query(User).filter(User.id == user_id,User.activate_user == True).first()

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        if user_data.name is not None:
            user.name = user_data.name

        if user_data.email is not None:
            user.email = user_data.email

        if user_data.age is not None:
            user.age = user_data.age

        if user_data.password is not None:
            user.hashed_password = hash_password(user_data.password)

        self.db.commit()
        self.db.refresh(user)

        return user
    
    def delete_user(self, user_id: int):

        user = self.db.query(User).filter(User.id == user_id,User.activate_user == True).first()

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        user.activate_user = False

        self.db.commit()

        return {"detail": "User deleted successfully"}
