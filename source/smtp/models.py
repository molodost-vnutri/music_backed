from pydantic import EmailStr

from source.settings import settings
from source.Core import BaseSMTPClient
from source.smtp.schemes import (
    SEND_FIRST_CHANGE_EMAIL,
    SEND_FORGOT_PASSWORD_USER,
    SEND_SECOND_CHANGE_EMAIL,
    SEND_VERIFY_MAIL,
    SEND_FORGOT_EMAIL
)


class SMTP_CreateFirst(BaseSMTPClient):
    subject = 'Завершение регистрации пользователя'
    
    def __init__(self, token: str, email: EmailStr):
        self.text = SEND_VERIFY_MAIL.format(settings.hostname, token)
        self.send_mail(email)



class SMTP_ChangeEmailFirst(BaseSMTPClient):
    subject = 'Смена почты на сервисе'
    def __init__(self, token: str, email: EmailStr) -> None:
        self.text = SEND_FIRST_CHANGE_EMAIL.format(settings.hostname, token)
        self.send_mail(email)


class SMTP_ChangeEmailSecond(BaseSMTPClient):
    subject = 'Смена почты на сервисе'
    def __init__(self, token: str, email: EmailStr) -> None:
        self.text = SEND_SECOND_CHANGE_EMAIL.format(settings.hostname, token)
        self.send_mail(email)


class SMTP_ChangePassword(BaseSMTPClient):
    subject = 'Смена пароля на сервисе'
    def __init__(self, token: str, email: EmailStr) -> None:
        self.text = SEND_FORGOT_PASSWORD_USER.format(settings.hostname, token)
        self.send_mail(email)


class SMTP_ChangeEmailModerator(BaseSMTPClient):
    subject = 'Смена пароля на сервисе'
    def __init__(self, token: str, email: EmailStr) -> None:
        self.text = SEND_FORGOT_EMAIL.format(settings.hostname, token)
        self.send_mail(email)
