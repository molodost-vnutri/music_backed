from source.users.crud import UserCRUD
from source.jwt.models import JWTCurrentUser
from source.users.schemes import SUserAuth
from source.users.services.password import verify_password
from source.exceptions import EmailOrPasswordIncorrectException

async def auth_current_user(request: SUserAuth):
    user = await UserCRUD.model_find_one(email=request.email)
    if not user:
        raise EmailOrPasswordIncorrectException
    if not verify_password(password=request.password, hash=user.password):
        raise EmailOrPasswordIncorrectException
    
    token = JWTCurrentUser.create_access_token(token={'sub': user.id}, days=3)
    return token