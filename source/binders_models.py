from sqlalchemy import Column, Integer, ForeignKey

from source.database import Base


class UserRolesModel(Base):
    __tablename__ = 'user_roles'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    role_id = Column(Integer, ForeignKey('roles.id'))


class UserMusicsModel(Base):
    __tablename__ = 'user_musics'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    music_id = Column(Integer, ForeignKey('musics.id'))


class MusicGenresModel(Base):
    __tablename__ = 'music_genres'
    id = Column(Integer, primary_key=True)
    music_id = Column(Integer, ForeignKey('musics.id'))
    genre_id = Column(Integer, ForeignKey('genres.id'))