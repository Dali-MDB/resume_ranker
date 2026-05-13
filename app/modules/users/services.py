from .repository import UserRepository
from core.dependencies import sessionDep
from .schemas import UserCreate, UserDisplay, UserUpdate
from core.security import oauth2_scheme
from .exceptions import UserDoesNotExist, UserAlreadyExists, UserNameTakenException, EmailTakenException, AuthenticationFailed
from fastapi import Depends
from .models import User
from typing import List, Annotated
from core.security import pwd_context, create_access_token, verify_access_token
from fastapi.security import OAuth2PasswordRequestForm

class UserService:
    def __init__(self, repo: UserRepository = Depends()):
        self.repo = repo


    def get_all_users(self, skip:int, limit: int)->List[User]:
        return self.repo.get_all_users(skip, limit)
            
    def get_user(self, id: int)->User:
        user = self.repo.fetch_user(id)
        if not user:
            raise UserDoesNotExist("this user could not be found")
        return user
    
    def register(self, user: UserCreate):
        #first we check if the user already exists
        if self.repo.check_if_user_exists(user.email, user.username):
            raise UserAlreadyExists("a user with this email or username already exist within our system")
        
        user_data = user.model_dump()
        user = User(**user_data)
        return self.repo.create(user)
    
    def update(self, id: int, user:UserUpdate):
        #first we query for the user
        user_db = self.repo.fetch_user(id)
        if not user_db:
            raise UserDoesNotExist("this user could not be found")
        
        user_data = user.model_dump(exclude_unset=True)
        #extract unique attributes

        #if the email is sent and   different from the current email  and already exists in the db (belongs to a different user)
        if user_data['email'] and user_db.email != user_data['email'] and self.repo.check_if_email_exists(user_data['email']):
            raise EmailTakenException(message="this email already exists")
        
        #if the username is sent and   different from the current username  and already exists in the db (belongs to a different user)
        if user_data['username'] and user_db.username != user_data['username'] and self.repo.check_if_username_exists(user_data['username']):
            raise UserNameTakenException(message="this username already exists")
        
        return self.repo.update(user_db, user_data)
        
    def delete(self, id:int):
        user = self.repo.fetch_user(id)
        self.repo.delete(user)
        
    
    def login(self, form_data : Annotated[OAuth2PasswordRequestForm,Depends()]):
        user = self.authenticate(form_data.username, form_data.password)
        if not user:
            raise AuthenticationFailed('we could not authenticate you, verify your username or password')
        
        data = {  #the payload to encode the jwt token
            'sub' : user.email,
            'user_id' : user.id   #to determine the current user
        }
        token = create_access_token(data)
        return  {
            "access_token" : token,
            "token_type" : "bearer"
        }

    

    def authenticate(self, email: str, password: str):
        user = self.repo.get_user_by_email(email)
        if not user:   #we don't tell that this account does not exist
            raise False
        if not pwd_context.verify(password, user.password):   #check the hash
            return False
        return user    #authenticated
        


