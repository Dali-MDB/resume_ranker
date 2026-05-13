from core.dependencies import sessionDep
from .models import User
from .schemas import UserCreate, UserUpdate, UserDisplay
from sqlalchemy import or_
from .exceptions import EmailTakenException, UserNameTakenException, UserDoesNotExist

class UserRepository:
    def create(self, db:sessionDep, user_data: UserCreate):
        #search if the user already exists
        user_already_exists = db.query(User).filter( or_(User.email == user_data.email , User.username ==  user_data.username)).first()
        if user_already_exists:
            return False
        user = User(**user_data.model_dump())
        db.add(user)
        db.commit()
        db.refresh(user)
        return UserDisplay(user)
    
    def update(self, db:sessionDep, user_id : int ,user_data: UserUpdate):
        #first we query for the user
        user = self.fetch_user(user_id, db)
        user_data = user_data.model_dump()
        #extract unique attributes
        if not user.email and user_data.email and not self.check_if_email_exists(user_data.email, db):
            raise EmailTakenException(message="this email already exists")
        if not user.username and user_data.username and  not self.check_if_username_exists(user_data.username, db):
            raise UserNameTakenException(message="this username already exists")
        for key, atr in user_data.model_dump(exclude_unset=True).items():
            setattr(user, key, atr)

        db.commit()
        db.refresh(user)
        return UserDisplay(User)
    
    def delete(self, db:sessionDep, user_id : int):
        user = self.fetch_user(user_id, db)
        db.delete(user)
        db.commit()

        

    def check_if_email_exists(new_email: str, db:sessionDep):
        if new_email:
            email_taken = db.query(User).filter(User.email == new_email).first()
            if email_taken:
                return False
        return True

    def check_if_username_exists(new_username: str, db: sessionDep):
        if new_username:
            username_taken = db.query(User).filter(User.email == new_username).first()
            if username_taken:
                return False
        return True
    
    def fetch_user(user_id: int, db: sessionDep):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise UserDoesNotExist("this user could not be found")
        return user


        