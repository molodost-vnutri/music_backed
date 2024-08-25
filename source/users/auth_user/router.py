from fastapi import APIRouter, Response, Depends

from source.users.auth_user.service import auth_current_user, forgot_password, change_password
from source.users.services.dependencies import check_auth_user, logout_user
from source.users.schemes import SUserAuthIn, SUserForgotPassword
router = APIRouter(
    prefix='/profile',
    tags=['Авторизация и деавторизация']
)

@router.post('/login', status_code=200)
async def auth_current_user_router(request: SUserAuthIn, response: Response, _ = Depends(check_auth_user)):
    token = await auth_current_user(request=request)
    response.set_cookie('access_token', token, httponly=True)
    return {
        'access_token': token
    }


@router.get('/logout', status_code=200)
def deauth_current_user_router(_ = Depends(logout_user)):
    return {
        'message': 'Деавторизован'
    }

@router.post('/forgot/password', status_code=200)
async def forgot_password_router(request: SUserForgotPassword, _ = Depends(check_auth_user)):
    return await forgot_password(request=request)

@router.get('/forgot/password/{}', status_code=200)
async def change_password(token: str, _ = Depends(check_auth_user)):
    return await change_password(token=token)