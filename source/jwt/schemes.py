from pydantic import BaseModel, EmailStr, PositiveInt

class SJWTBase(BaseModel):
    exp: float

class SJWTCurrentUser(SJWTBase):
    sub: PositiveInt

class SJWTCreateFirst(SJWTBase):
    email: EmailStr
    session: str

class SJWTChangeEmail(SJWTBase):
    email: EmailStr


class SJWTChangeEmailModerator(SJWTChangeEmail, SJWTCurrentUser):
    pass

class SJWTChangePassword(SJWTCreateFirst):
    pass