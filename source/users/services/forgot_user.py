from source.exceptions import EmailNotFoundException, UserNotFoundException
from source.users.crud import UserCRUD
from source.users.services.password import hashed_password
from source.users.schemes import SUserForgotPassword, SUserChangeForgotPassword
from source.smtp.models import SMTP_ChangePassword
from source.jwt.models import JWTChangePassword

async def forgot_password(request: SUserForgotPassword):
    user_exist = await UserCRUD.model_find_one(email=request.email)
    if not user_exist:
        raise EmailNotFoundException
    token = JWTChangePassword.create_access_token(token={'email': request.email}, minutes=15)
    SMTP_ChangePassword(token=token, email=request.email)

async def change_password(token: str, request: SUserChangeForgotPassword):
    decode_token = JWTChangePassword.decode_token(token)
    user_exist = await UserCRUD.model_find_one(email=decode_token.email)
    if not user_exist:
        raise UserNotFoundException
    password = hashed_password(request.new_password)
    await UserCRUD.model_update(model_id=user_exist.id, password=password)