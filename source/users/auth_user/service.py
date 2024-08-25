from source.users.schemes import SUserAuthIn, SUserForgotPassword
from source.users.crud import UserCRUD
from source.exceptions import EmailOrPasswordIncorrectException, UserBannedException, EmailNotFoundException
from source.jwt.models import JWTCurrentUser, JWTChangePassword
from source.users.services.password import verify_password, get_password_hash
from source.CRUD_schemes import SUserPGOut
from source.smtp.models import SMTP_ChangePassword


async def auth_current_user(request: SUserAuthIn):
    user: SUserPGOut = await UserCRUD.model_find_one(email=request.email)
    if not user:
        raise EmailOrPasswordIncorrectException
    if user.banned:
        raise UserBannedException
    if not verify_password(request.password, user.password):
        raise EmailOrPasswordIncorrectException
    return JWTCurrentUser.create_access_token(token={'sub': user.id}, days=3)


async def forgot_password(request: SUserForgotPassword):
    user: SUserPGOut = await UserCRUD.model_find_one(email=request.email)
    if not user:
        raise EmailNotFoundException
    password = get_password_hash(request.new_password)
    token = JWTChangePassword.create_access_token({'email': request.email, 'session': password})
    SMTP_ChangePassword(token=token, email=request.email)
    return {
        'message': 'Письмо отправлено на почту'
    }

async def change_password(token: str):
    payload = JWTChangePassword.decode_token(token)
    user: SUserPGOut = await UserCRUD.model_find_one(email=payload.email)
    if not user:
        raise EmailNotFoundException
    await UserCRUD.model_update(model_id=user.id, password=payload.session)
    return {
        'message': 'Пароль изменён'
    }