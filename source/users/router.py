from fastapi import APIRouter, Response, Depends
from source.users.schemes import SUserCreateFirst, SUserCreateSecond, SUserAuth, SUserChangePassword, SUserChangeEmail
from source.users.services.create_user import send_registration_link, create_user_second
from source.users.services.auth_user import auth_current_user
from source.users.services.dependencies import get_current_user
from source.users.services.current_user import (
    get_roles_current_user,
    change_username_current_user,
    change_password_current_user,
    change_email_current_user_first,
    change_email_current_user_second,
    change_email_current_user_last
)

router = APIRouter(
    prefix='/profile',
    tags=['Пользователи']
)

@router.post('', status_code=200)
async def create_user_first_router(request: SUserCreateFirst):
    await send_registration_link(request=request)
    return {
        'message': 'Если почта существует, то на данные email будет отправлена ссылка для завершения регистрации'
    }

@router.post('/verify/mail/{token}', status_code=201)
async def create_user_second_router(token: str, request: SUserCreateSecond):
    await create_user_second(token=token, request=request)
    return {
        'message': 'Почта успешно верифицирована'
    }

@router.post('/auth', status_code=200)
async def auth_user_router(request: SUserAuth, response: Response):
    token = await auth_current_user(request=request)
    response.set_cookie('access_token', token, httponly=True)
    return {
        'access_token': token
    }

@router.get('/information', status_code=200)
async def get_information_current_user_router(user_id: int = Depends(get_current_user)):
    return await get_roles_current_user(user_id=user_id)

@router.patch('/change/username', status_code=200)
async def change_username_current_user_router(username: str, user_id = Depends(get_current_user)):
    await change_username_current_user(user_id=user_id, username=username)
    return {
        'message': 'Юзернейм успешно изменён'
    }

@router.patch('/change/password', status_code=200)
async def change_password_current_user_router(payload: SUserChangePassword, response: Response, user_id = Depends(get_current_user)):
    await change_password_current_user(user_id=user_id, request=payload)
    response.delete_cookie('access_token')
    return {
        'message': 'Пароль успешно изменён'
    }

@router.post('/change/email/first', status_code=200)
async def change_email_current_user_first_router(request: SUserChangeEmail, _ = Depends(get_current_user)):
    await change_email_current_user_first(email=request.new_email)
    return {
        'message': 'Письмо отправлено на основную почту'
    }

@router.get('/change/email/second/{token}', status_code=200)
async def change_email_current_user_second_router(token: str, _ = Depends(get_current_user)):
    await change_email_current_user_second(token=token)
    return {
        'message': 'Письмо отправлено на почту указанную в форме'
    }

@router.patch('/change/email/last/{token}', status_code=201)
async def change_email_current_user_last_router(token: str, user_id = Depends(get_current_user)):
    await change_email_current_user_last(token=token, user_id=user_id)
    return {
        'message': 'Почта успешно подтверждена'
    }