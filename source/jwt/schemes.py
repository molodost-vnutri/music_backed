from pydantic import BaseModel, EmailStr

class SJWTBase(BaseModel):
    exp: float

class SJWTCurrentUser(SJWTBase):
    sub: int

class SJWTCreateUserFirst(SJWTBase):
    email: EmailStr
