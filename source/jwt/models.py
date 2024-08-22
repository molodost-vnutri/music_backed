from source.Core import BaseJWT
from source.jwt.schemes import SJWTCreateUserFirst, SJWTCurrentUser

class JWTCreateFirst(BaseJWT):
    scheme_validator = SJWTCreateUserFirst

class JWTCurrentUser(BaseJWT):
    scheme_validator = SJWTCurrentUser

class JWTChangeEmailFirst(JWTCreateFirst):
    pass

class JWTChangeEmailSecond(JWTCreateFirst):
    pass

class JWTChangeEmailLast(JWTCreateFirst):
    pass