from fastapi import APIRouter
from .repository import UserRepository


router = APIRouter(
    prefix='/users',
    tags=['users'],
)
