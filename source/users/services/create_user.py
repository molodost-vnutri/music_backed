from source.exceptions import EmailAlreadyException

from source.smtp.models import SMTP_CreateFirst
from source.jwt.models import JWTCreateFirst
from source.users.schemes import SUserCreateFirst, SUserCreateSecond
from source.users.crud import UserCRUD, UserRolesCRUD
from source.users.services.password import hashed_password


async def send_registration_link(request: 'SUserCreateFirst'):
    if await UserCRUD.model_find_one(email=request.email):
        return
    token = JWTCreateFirst.create_access_token(token={'email': request.email}, minutes=15)
    SMTP_CreateFirst(token=token, email=request.email)

async def create_user_second(request: SUserCreateSecond, token: str):
    payload = JWTCreateFirst.decode_token(token=token)
    
    if await UserCRUD.model_find_one(email=payload.email):
        raise EmailAlreadyException
    
    password = hashed_password(request.password)
    
    user_id = await UserCRUD.model_insert(
        email=payload.email,
        password=password
    )
    
    await UserRolesCRUD.model_insert(
        user_id=user_id,
        role_id=1
    )