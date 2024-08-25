from source.Core import BaseJWT
from source.jwt.schemes import SJWTCreateFirst, SJWTCurrentUser, SJWTChangeEmail, SJWTChangeEmailModerator


class JWTCreateFirst(BaseJWT[SJWTCreateFirst]):
    scheme_validator = SJWTCreateFirst


class JWTCurrentUser(BaseJWT[SJWTCurrentUser]):
    scheme_validator = SJWTCurrentUser


class JWTChangeEmailFirst(JWTCreateFirst):
    pass


class JWTChangeEmailSecond(BaseJWT[SJWTChangeEmail]):
    scheme_validator = SJWTChangeEmail


class JWTChangeEmailLast(JWTChangeEmailSecond):
    pass


class JWTChangePassword(JWTChangeEmailSecond):
    pass


class JWTChangeEmailModerator(JWTChangeEmailSecond):
    scheme_validator = SJWTChangeEmailModerator