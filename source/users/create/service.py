from source.exceptions import EmailAlreadyException

from source.smtp.models import SMTP_CreateFirst

from source.jwt.models import JWTCreateFirst

from source.users.schemes import SUserCreateFirst
from source.users.crud import UserCRUD
from source.users.services.password import get_password_hash


async def send_registration_link(request: SUserCreateFirst):
    if await UserCRUD.model_find_one(email=request.email):
        raise EmailAlreadyException
    
    password = get_password_hash(request.password)
    
    token = JWTCreateFirst.create_access_token(token={'email': request.email, 'session': password}, minutes=15)

    SMTP_CreateFirst(token, request.email)

    return {
        'message': 'Письмо отправлено на указанную почту'
    }

async def create_user(token: str):
    payload = JWTCreateFirst.decode_token(token)

    if await UserCRUD.model_find_one(email=payload.email):
        raise EmailAlreadyException


    await UserCRUD.model_insert(email=payload.email, hash_password=payload.session)
    return {
        'message': 'Почта успешно зарегистрирована'
    }