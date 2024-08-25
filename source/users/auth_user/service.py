from source.users.schemes import SUserAuthIn
from source.users.crud import UserCRUD
from source.exceptions import EmailOrPasswordIncorrectException, UserBannedException
from source.jwt.models import JWTCurrentUser
from source.users.services.password import verify_password
from source.CRUD_schemes import SUserPGOut


async def auth_current_user(request: SUserAuthIn):
    user: SUserPGOut = await UserCRUD.model_find_one(email=request.email)
    if not user:
        raise EmailOrPasswordIncorrectException
    if user.banned:
        raise UserBannedException
    if not verify_password(request.password, user.password):
        raise EmailOrPasswordIncorrectException
    return JWTCurrentUser.create_access_token(token={'sub': user.id}, days=3)
