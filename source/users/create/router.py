from fastapi import APIRouter, Depends

from source.users.schemes import SUserCreateFirst
from source.users.create.service import send_registration_link, create_user
from source.users.services.dependencies import check_auth_user

router = APIRouter(
    prefix='/profile',
    tags=['Регистрация пользователя']
)


@router.post('', status_code=200)
async def send_verification_mail_router(request: SUserCreateFirst, _ = Depends(check_auth_user)):
    return await send_registration_link(request)


@router.get('/verify/email/{token}', status_code=201, include_in_schema=False)
async def create_user_router(token: str, _ = Depends(check_auth_user)):
    return await create_user(token=token)
