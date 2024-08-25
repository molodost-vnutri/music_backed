from datetime import datetime, UTC, timedelta
from typing import Type, Dict, AnyStr, TypeVar, Generic
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from sqlalchemy import insert, select, update, delete
from pydantic import BaseModel, EmailStr, PositiveInt
from jwt import decode, encode

from source.database import async_session
from source.settings import settings
from source.jwt.schemes import SJWTBase
from source.exceptions import (
    ExpireJWTException,
    IncorrectJWTException
)


T = TypeVar('T', bound=BaseModel)

class BaseCRUD:
    model = None


    @classmethod
    async def model_find_one(cls, **arg):
        async with async_session() as session:
            query = select(cls.model).filter_by(**arg)
            result = await session.execute(query)
            return result.scalar_one_or_none()
    

    @classmethod
    async def model_find_all(cls, **arg):
        async with async_session() as session:
            query = select(cls.model).filter_by(**arg)
            result = await session.execute(query)
            return result.scalars().all()
    

    @classmethod
    async def model_insert(cls, **arg):
        async with async_session() as session:
            query = insert(cls.model).values(**arg).returning(cls.model)
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one()
    

    @classmethod
    async def model_update(cls, model_id: PositiveInt, **arg):
        async with async_session() as session:
            query = update(cls.model).filter_by(id=model_id).values(**arg).returning(cls.model)
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one()
        

    @classmethod
    async def model_delete(cls, model_id: PositiveInt):
        async with async_session() as session:
            query = delete(cls.model).filter_by(id=model_id).returning(cls.model)
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one()
        

class BaseJWT(Generic[T]):
    scheme_validator: Type[SJWTBase] = None

    @classmethod
    def decode_token(cls, token: str) -> T:
        try:
            payload: dict = decode(
                jwt=token,
                key=settings.secret_key,
                algorithms=[settings.algorithm]
            )
            exp_payload = str(payload['exp'])
            payload['exp'] = exp_payload
            scheme = cls.scheme_validator.model_validate(payload)
        except:
            raise IncorrectJWTException
        
        if datetime.now(UTC) > datetime.fromtimestamp(scheme.exp, tz=UTC):
            raise ExpireJWTException
        
        return scheme
    
    @staticmethod
    def create_access_token(token: dict, **time) -> str:
        encode_jwt = token.copy()
        expired = datetime.now(UTC) + timedelta(**time)
        encode_jwt.update({'exp': expired})
        jwt_token = encode(
            payload=encode_jwt,
            key=settings.secret_key,
            algorithm=settings.algorithm
        )
        return jwt_token

class BaseSMTPClient:
    subject: AnyStr
    text: AnyStr
    
    def send_mail(self, email: EmailStr):
        message = MIMEMultipart()
        message['From'] = settings.smtp_mail
        message['To'] = email
        message['Subject'] = self.subject
        message.attach(MIMEText(self.text, 'plain'))
        try:
            with SMTP_SSL(settings.smtp_host, settings.smtp_port) as client:
                client.login(settings.smtp_mail, settings.smtp_pass)
                client.sendmail(settings.smtp_mail, email, message.as_string())
        except:
            pass
