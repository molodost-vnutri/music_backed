from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from source.settings import settings

engine = create_async_engine(url=settings.postgres_url)

async_session = async_sessionmaker(bind=engine, class_=AsyncSession)

class Base(DeclarativeBase):
    pass