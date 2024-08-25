from sqlalchemy import Column, Integer, String

from source.database import Base

class MusicModel(Base):
    __tablename__ = 'musics'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    albom = Column(String)
    artist = Column(String, nullable=False)
    path = Column(String, unique=True, nullable=False)
    hash = Column(String, unique=True, nullable=False)


class GenreModel(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True)
    genre = Column(String, unique=True)