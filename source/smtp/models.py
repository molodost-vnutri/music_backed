from pydantic import EmailStr

from source.settings import settings
from source.Core import BaseSMTPClient
from source.smtp.schemes import SEND_VERIFY_MAIL, SEND_FIRST_CHANGE_EMAIL, SEND_SECOND_CHANGE_EMAIL, SEND_FORGOT_PASSWORD_USER

class SMTP_CreateFirst(BaseSMTPClient):
    body = SEND_VERIFY_MAIL
    subject = 'Завершение регистрации пользователя'
    def __init__(self, token: str, email: EmailStr):
        self.body = SEND_VERIFY_MAIL.format(settings.hostname, token, settings.hostname)
        self.send_mail(email=email, body=self.body, subject=self.subject)

class SMTP_ChangeFirst(BaseSMTPClient):
    body = SEND_FIRST_CHANGE_EMAIL
    subject = 'Смена почты на сервисе'
    def __init__(self, token: str, email: EmailStr):
        self.body = self.body.format(settings.hostname, token)
        self.send_mail(email=email, body=self.body, subject=self.subject)

class SMTP_ChangeSecond(BaseSMTPClient):
    body = SEND_SECOND_CHANGE_EMAIL
    subject = 'Смена почты на сервисе'
    def __init__(self, token: str, email: EmailStr):
        self.body = self.body.format(settings.hostname, token)
        self.send_mail(email=email, body=self.body, subject=self.subject)

class SMTP_ChangePassword(BaseSMTPClient):
    body = SEND_FORGOT_PASSWORD_USER
    subject = 'Смена пароля на сервисе'
    def __init__(self, token: str, email: EmailStr):
        self.body = self.body.format(settings.hostname, token)
        self.send_mail(email=email, body=self.body, subject=self.subject)
