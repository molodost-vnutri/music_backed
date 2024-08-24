from typing import Optional

from fastapi import Request, Depends

from source.exceptions import JWTNotFound, NotFoundException, UserNotFoundException, UserAlreadyAuthException
from source.users.crud import UserCRUD
from source.jwt.models import JWTCurrentUser
from source.users.schemes import SUserInformation

def get_token(response: Request) -> Optional[str]:
    return response.cookies.get('access_token')

async def get_current_user(token = Depends(get_token)):
    if not token:
        raise JWTNotFound
    token_decode = JWTCurrentUser.decode_token(token)
    user_exist = await UserCRUD.model_find_one(id=token_decode.sub)
    if user_exist:
        return token_decode.sub
    raise UserNotFoundException

async def check_current_admin(token = Depends(get_token)):
    if not token:
        raise NotFoundException
    user_id = JWTCurrentUser.decode_token(token).sub
    user: SUserInformation = await UserCRUD.model_get_current_user(model_id=user_id)
    if not any(role == 'Администратор' for role in user.roles):
        raise NotFoundException
    return user_id

def check_unauth_user(token = Depends(get_token)):
    if not token:
        return True
    raise UserAlreadyAuthException