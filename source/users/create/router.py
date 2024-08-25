from fastapi import APIRouter

from source.users.schemes import SUserCreateFirst
from source.users.create.service import send_registration_link, create_user


router = APIRouter(
    prefix='/profile',
    tags=['Регистрация пользователя']
)


@router.post('', status_code=200)
async def send_verification_mail_router(request: SUserCreateFirst):
    return await send_registration_link(request)


@router.get('/verify/email/{token}', status_code=201, include_in_schema=False)
async def create_user_router(token: str):
    return await create_user(token=token)
