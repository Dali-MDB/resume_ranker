from fastapi import APIRouter
from .services import UserService
from .schemas import UserCreate, UserUpdate, UserDisplay, RefreshTokenResponse
from typing import Annotated, List
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse


router = APIRouter(
    prefix='/users',
    tags=['users'],
)


@router.get('', response_model=List[UserDisplay])
async def get_all_user( skip:int = 0, limit: int = 20, service: UserService = Depends()):
    users = service.get_all_users(skip, limit)
    return users


@router.get('/{user_id}', response_model=UserDisplay)
async def get_user(user_id:int, service: UserService = Depends()):
    user = service.get_user(user_id)
    return user


@router.post('/register', response_model= UserDisplay)
async def register(user: UserCreate, service: UserService = Depends()):
    user = service.register(user)
    return user


@router.post('/login', response_model= RefreshTokenResponse)
async def login(form_data : Annotated[OAuth2PasswordRequestForm, Depends()], service: UserService = Depends()):
    response = service.login(form_data)
    return response


@router.put('/{user_id}', response_model=UserDisplay)
async def update_user(user_id: int, user: UserUpdate, service: UserService = Depends()):
    user = service.update(user_id, user)
    return user


@router.delete('/{user_id}')
async def delete_user(user_id: int, service: UserService = Depends()):
    service.delete(user_id)
    return JSONResponse(
        content={
            'message' : 'the user has been deleted successfully'
        }
    )