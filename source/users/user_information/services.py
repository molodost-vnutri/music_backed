from pydantic import PositiveInt

from source.exceptions import EmailAlreadyException, EmailAlreadyUsedException
from source.smtp.models import SMTP_ChangeEmailFirst, SMTP_ChangeEmailSecond
from source.jwt.models import JWTChangeEmailFirst, JWTChangeEmailLast, JWTChangeEmailSecond
from source.users.crud import UserCRUD
from source.users.schemes import SUserChangeEmail


async def change_email_first(request: SUserChangeEmail, user_id: PositiveInt):
    user = await UserCRUD.model_find_one(id=user_id)
    if request.new_email == user.email:
        raise EmailAlreadyUsedException
    email_exist = await UserCRUD.model_find_one(email=request.new_email)
    if email_exist:
        raise EmailAlreadyException
    token = JWTChangeEmailFirst.create_access_token(token={'email': request.new_email}, minutes=15)
    SMTP_ChangeEmailFirst(token, email=user.email)
    return {
        'message': 'Ссылка отправлена на основную почту'
    }

async def change_email_second(token: str):
    payload = JWTChangeEmailFirst.decode_token(token)
    email_exist = await UserCRUD.model_find_one(email=payload.email)
    if email_exist:
        raise EmailAlreadyException
    token = JWTChangeEmailSecond.create_access_token(token={'email': payload.email}, minutes=15)
    SMTP_ChangeEmailSecond(token=token, email=payload.email)
    return {
        'message': 'Ссылка отправлена на указанную почту'
    }

async def change_email_last(token: str, user_id: PositiveInt):
    payload = JWTChangeEmailLast.decode_token(token)
    email_exist = await UserCRUD.model_find_one(email=payload.email)
    if email_exist:
        raise EmailAlreadyException
    await UserCRUD.model_update(model_id=user_id, email=payload.email)
    return {
        'message': 'Почта успешно изменена'
    }