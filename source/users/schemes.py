from typing import List, Optional
from re import search

from pydantic import BaseModel, field_validator, EmailStr

from source.exceptions import (
    PasswordLowerCaseException,
    PasswordCharException,
    PasswordLengthException,
    PasswordNumException,
    PasswordUpperCaseException,
    PasswordNotAsciiException

)

class SUserAuth(BaseModel):
    email: EmailStr
    password: str

class SUserCreateFirst(BaseModel):
    email: EmailStr

class SUserCreateSecond(BaseModel):
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

class SUserInformation(BaseModel):
    roles: List
    username: Optional[str]
    email: EmailStr
    created_at: str
    updated_at: str
    class Config:
        from_attributes = True

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