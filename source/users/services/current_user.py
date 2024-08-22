from pydantic import EmailStr

from source.users.crud import UserCRUD
from source.users.schemes import SUserChangePassword
from source.users.services.password import verify_password, hashed_password
from source.smtp.models import SMTP_ChangeFirst, SMTP_ChangeSecond
from source.exceptions import OldPasswordIncorrectException, PasswordsMatchException, EmailAlreadyException
from source.jwt.models import JWTChangeEmailFirst, JWTChangeEmailSecond, JWTChangeEmailLast

async def get_roles_current_user(user_id: int):
    return await UserCRUD.model_get_current_user(model_id=user_id)

async def change_username_current_user(user_id: int, username: str):
    await UserCRUD.model_update(model_id=user_id, username=username)

async def change_password_current_user(user_id: int, request: SUserChangePassword):
    if request.old_password == request.new_password:
        raise PasswordsMatchException
    current_user = await UserCRUD.model_find_one(id=user_id)
    if not verify_password(password=request.old_password, hash=current_user.password):
        raise OldPasswordIncorrectException
    password = hashed_password(password=request.new_password)
    await UserCRUD.model_update(model_id=user_id, password=password)

async def change_email_current_user_first(email: EmailStr):
    email_exist = await UserCRUD.model_find_one(email=email)
    if email_exist:
        raise EmailAlreadyException
    token = JWTChangeEmailFirst.create_access_token(token={'email': email}, minutes=15)
    SMTP_ChangeFirst(token=token, email=email)

async def change_email_current_user_second(token: str):
    payload = JWTChangeEmailFirst.decode_token(token=token)
    email_exist = await UserCRUD.model_find_one(email=payload.email)
    if email_exist:
        raise EmailAlreadyException
    token = JWTChangeEmailSecond.create_access_token(token={'email': payload.email}, minutes=15)
    SMTP_ChangeSecond(email=payload.email, token=token)

async def change_email_current_user_last(token: str, user_id: int):
    payload = JWTChangeEmailLast.decode_token(token=token)
    await UserCRUD.model_update(model_id=user_id, email=payload.email)