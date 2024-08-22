from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from source.database import Base

class MusicModel(Base):
    __tablename__ = 'musics'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    albom = Column(String)
    artist = Column(String)
    path = Column(String, unique=True)

    genres = relationship('MusicGenreModel', back_populates='music')

class GenreModel(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True)
    genre = Column(String, unique=True)

class MusicGenreModel(Base):
    __tablename__ = 'music_genres'
    id = Column(Integer, primary_key=True)
    music_id = Column(Integer, ForeignKey('musics.id'))
    genre_id = Column(Integer, ForeignKey('genres.id'))

    music = relationship('MusicModel', back_populates='genres')