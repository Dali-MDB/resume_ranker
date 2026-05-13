from app.core.dependencies import sessionDep
from .models import User
from .schemas import UserCreate, UserUpdate, UserDisplay
from sqlalchemy import or_
from .exceptions import EmailTakenException, UserNameTakenException, UserDoesNotExist, UserAlreadyExists
from typing import List

class UserRepository:
    def __init__(self, db:sessionDep):
        self.db = db
    def create(self, user: User)->User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def update(self, user: User, user_data: dict)->User:
        for key, atr in user_data.items():
            setattr(user, key, atr)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    
    def delete(self, user : User):
        #user = self.fetch_user(user_id, self.db)
        self.db.delete(user)
        self.db.commit()

    def get_all_users(self, skip: int, limit:int) ->List[User]:
        return self.db.query(User).offset(skip).limit(limit).all()
    
    def check_if_user_exists(self, email: str, username: str)->bool:
        return self.db.query(User).filter( or_(User.email == email , User.username ==  username)).first()
        
    def check_if_email_exists(self, new_email: str)->bool:
        return self.db.query(User).filter(User.email == new_email).first()
        if email_taken:
                return False
        return True

    def check_if_username_exists(self, new_username: str)->bool:
        return self.db.query(User).filter(User.email == new_username).first()
        if username_taken:
                return False
        return True
    
    def fetch_user(self, user_id: int)->User:
        return self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise UserDoesNotExist("this user could not be found")
        return user

    def get_user_by_email(self, email: str)->User:
        return self.db.query(User).filter(User.email == email).first()


        
