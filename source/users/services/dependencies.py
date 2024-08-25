from typing import Optional, List

from fastapi import Request, Depends, Response
from pydantic import PositiveInt

from source.users.crud import UserCRUD
from source.CRUD_schemes import SUserPGOut
from source.jwt.models import JWTCurrentUser
from source.exceptions import (
    JWTNotFound,
    NotFoundException,
    UserNotFound,
    UserAlreadyAuthException,
    UserNotAuthException,
    UserBanned
)


def get_token(request: Request) -> Optional[str]:
    return request.cookies.get('access_token')

async def get_current_user(response: Response, token = Depends(get_token)):
    if not token:
        raise JWTNotFound
    
    token_decode = JWTCurrentUser.decode_token(token)
    user_exist: SUserPGOut = await UserCRUD.model_find_one(id=token_decode.sub)
    if user_exist and not user_exist.banned:
        return token_decode.sub
    response.delete_cookie('access_token')
    if not user_exist:
        return UserNotFound
    return UserBanned
    

def check_auth_user(token = Depends(get_token)):
    if token:
        raise UserAlreadyAuthException

def logout_user(response: Response, token = Depends(get_token)):
    if not token:
        raise UserNotAuthException
    response.delete_cookie('access_token')

async def check_current_depend(token = Depends(get_token)):
    if not token:
        raise NotFoundException
    user_id = JWTCurrentUser.decode_token(token).sub
    user_roles: List[PositiveInt] = await UserCRUD.get_all_roles_id(model_id=user_id)
    if not any(2 == role or 3 == role for role in user_roles):
        raise NotFoundException
    return user_id

async def check_admin_depend(token = Depends(get_current_user)):
    if not token:
        raise NotFoundException
    user_id = JWTCurrentUser.decode_token(token).sub
    user_roles: List[PositiveInt] = await UserCRUD.get_all_roles_id(model_id=user_id)
    if not any(3 == role for role in user_roles):
        raise NotFoundException
    return user_id