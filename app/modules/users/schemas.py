from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    email: str
    username: str


class UserCreate(UserBase):
    password : str

class UserDisplay(UserBase):
    id : int
    date_joined : datetime








