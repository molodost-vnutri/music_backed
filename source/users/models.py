from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from source.database import Base

class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, nullable=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

    roles = relationship('UserRolesModel', back_populates='user', primaryjoin="and_(UserModel.id==UserRolesModel.user_id)")
    musics = relationship('UserMusicsModel', back_populates='user', primaryjoin='and_(UserModel.id==UserMusicsModel.user_id)')

class RoleModel(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    role = Column(String, unique=True)

class UserRolesModel(Base):
    __tablename__ = 'user_roles'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    role_id = Column(Integer, ForeignKey('roles.id'))

    user = relationship('UserModel', back_populates='roles')

class UserMusicsModel(Base):
    __tablename__ = 'user_musics'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    music_id = Column(Integer, ForeignKey('musics.id'))

    user = relationship('UserModel', back_populates='musics')