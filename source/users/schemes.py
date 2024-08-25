from typing import List, Optional
from re import search

from pydantic import BaseModel, field_validator, EmailStr, PositiveInt

from source.exceptions import (
    PasswordLowerCaseException,
    PasswordCharException,
    PasswordLengthException,
    PasswordNotAsciiException,
    PasswordNumException,
    PasswordUpperCaseException,
)


class SUserAuthIn(BaseModel):
    email: EmailStr
    password: str


class SUserCreateFirst(BaseModel):
    email: EmailStr
    password: str

    @field_validator('password')
    def validation_passwords(cls, v: str) -> str:
        if not v.isascii():
            raise PasswordNotAsciiException
        if not (12 <= len(v) <= 30):
            raise PasswordLengthException
        if not search(r'[a-z]', v):
            raise PasswordLowerCaseException
        if not search(r'[A-Z]', v):
            raise PasswordUpperCaseException
        if not search(r'[0-9]', v):
            raise PasswordNumException
        if not search(r'\W', v):
            raise PasswordCharException
        return v


class SUserAuthOut(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: EmailStr
    created_at: str
    updated_at: str
    roles: List[str]
    
    class Config:
        from_atributes = True


class SUserChangePassword(BaseModel):
    old_password: str
    new_password: str

    @field_validator('new_password')
    def validation_passwords(cls, v: str) -> str:
        if not v.isascii():
            raise PasswordNotAsciiException
        if not (12 <= len(v) <= 30):
            raise PasswordLengthException
        if not search(r'[a-z]', v):
            raise PasswordLowerCaseException
        if not search(r'[A-Z]', v):
            raise PasswordUpperCaseException
        if not search(r'[0-9]', v):
            raise PasswordNumException
        if not search(r'\W', v):
            raise PasswordCharException
        return v


class SUserChangeEmail(BaseModel):
    new_email: EmailStr


class SUserForgotPassword(BaseModel):
    email: EmailStr


class SUserChangeForgotPassword(BaseModel):
    new_password: str

    @field_validator('new_password')
    def validation_passwords(cls, v: str) -> str:
        if not v.isascii():
            raise PasswordNotAsciiException
        if not (12 <= len(v) <= 30):
            raise PasswordLengthException
        if not search(r'[a-z]', v):
            raise PasswordLowerCaseException
        if not search(r'[A-Z]', v):
            raise PasswordUpperCaseException
        if not search(r'[0-9]', v):
            raise PasswordNumException
        if not search(r'\W', v):
            raise PasswordCharException
        return v


class SChangeUsername(BaseModel):
    username: str


class SChangeFi(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]


class SBannedUser(BaseModel):
    user_id: PositiveInt


class SUnbannedUser(SBannedUser):
    pass

class SChangePasswordModerator(SBannedUser):
    pass

class SChangeEmailModerator(SUserForgotPassword, SBannedUser):
    pass

class SUserModeratorOut(BaseModel):
    id: PositiveInt
    email: EmailStr
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    created_at: str
    updated_at: str
    banned: bool

    class Config:
        from_atributes = True
