from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean

from source.database import Base


class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime, onupdate=datetime.now())
    banned = Column(Boolean)


class RoleModel(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    role = Column(String, unique=True)