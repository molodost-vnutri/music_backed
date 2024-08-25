from string import ascii_lowercase, ascii_uppercase, punctuation
from random import choice, choices, randint, shuffle

from pydantic import PositiveInt, EmailStr

from source.exceptions import ModeratorNotBannedSelfException, NotHavePermissionException, UserNotExistException, ModeratorNotUnbannedSelfException, ModeratorNotDeleteSelfException
from source.jwt.models import JWTChangeEmailModerator
from source.users.services.password import get_password_hash
from source.smtp.models import SMTP_ChangeEmailModerator
from source.users.crud import UserCRUD


async def check_permission(model_id: PositiveInt):
    user_roles = await UserCRUD.get_all_roles_id(model_id)
    if not user_roles:
        raise UserNotExistException
    if any(2 == role or 3 == role for role in user_roles):
        raise NotHavePermissionException


async def banned_user(model_id: PositiveInt, moderator_id: PositiveInt):
    if model_id == moderator_id:
        raise ModeratorNotBannedSelfException
    await check_permission(model_id)
    await UserCRUD.model_update(model_id=model_id, banned=True)
    return {
        'message': 'Пользователь с id {} забанен'.format(model_id)
    }

async def unbanned_user(model_id: PositiveInt, moderator_id: PositiveInt):
    if model_id == moderator_id:
        raise ModeratorNotUnbannedSelfException
    await check_permission(model_id)
    await UserCRUD.model_update(model_id=model_id, banned=False)
    return {
        'message': 'Пользователь с id {} разбанен'.format(model_id)
    }

async def change_password(model_id: PositiveInt):
    await check_permission(model_id)
    lowercase_letters = ascii_lowercase
    uppercase_letters = ascii_uppercase
    digits = digits
    special_characters = punctuation

    length = randint(12, 30) 

    password = [
        choice(lowercase_letters),
        choice(uppercase_letters),
        choice(digits),
        choice(special_characters)
    ]
    all_characters = lowercase_letters + uppercase_letters + digits + special_characters
    password.extend(choices(all_characters, k=length - 4))
    shuffle(password)
    password = ''.join(password)
    hashed_password = get_password_hash(password)
    user = await UserCRUD.model_update(model_id=model_id, password=hashed_password)
    return {
        'message': 'Пароль пользователя с email {} изменён на {}'.format(user.email, password)
    }

async def change_email(model_id: PositiveInt, email: EmailStr):
    await check_permission(model_id=model_id)
    user = await UserCRUD.model_find_one(id=model_id)
    token = JWTChangeEmailModerator.create_access_token(token={'email': email, 'sub': user.id}, hours=3)
    SMTP_ChangeEmailModerator(token=token, email=email)
    return {
        'message': 'На новую почту отправлена ссылка на подтверждение почты'
    }