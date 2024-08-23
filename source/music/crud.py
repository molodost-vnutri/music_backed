from sqlalchemy import select, insert

from source.exceptions import GenreNotFoundException, RollbackException
from source.Core import BaseCRUD, invert_dict
from source.database import async_session
from source.music.models import MusicGenreModel, MusicModel, GenreModel, MusicEndModel

class MusicCRUD(BaseCRUD):
    model = MusicModel

    @classmethod
    async def model_insert(cls, session, **arg):
        query = insert(cls.model).values(**arg).returning(cls.model.id)
        result = await session.execute(query)
        return result.scalar_one()

    @classmethod
    async def model_get_music_current_user(cls, model_id: int):
        async with async_session() as session:
            query = (
                select(cls.model, GenreModel.genre)
                .join(MusicGenreModel, cls.model.id == MusicGenreModel.music_id)
                .join(GenreModel, MusicGenreModel.genre_id == GenreModel.id)
                .filter(cls.model.id == model_id)
            )

            result = await session.execute(query)
            music_info = result.mappings().all()

            musics = [row[cls.model.__tablename__] for row in music_info]

            return musics
    
    @classmethod
    async def model_music_insert(cls, name, albom, artist, path, id_, hash):
        async with async_session() as session:
            try:
                async with session.begin():
                    music_id = await cls.model_insert(
                        session=session,
                        name=name,
                        albom=albom,
                        artist=artist,
                        path=path,
                        hash=hash
                    )
                    await MusicGenreCRUD.model_insert(session=session, music_id=music_id, genre_id=id_)
            except:
                raise RollbackException


                    

class MusicGenreCRUD(BaseCRUD):
    model = MusicGenreModel

    @classmethod
    async def model_find_all(cls, **arg):
        async with async_session() as session:
            query = select(cls.model).filter_by(**arg)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def model_insert(cls, session, **arg):
        query = insert(cls.model).values(**arg).returning(cls.model.id)
        result = await session.execute(query)
        return result.scalar_one()

class GenreCRUD(BaseCRUD):
    model = GenreModel

class MusicEndCRUD(BaseCRUD):
    model = MusicEndModel

    @classmethod
    async def model_find_all(cls, **arg):
        async with async_session() as session:
            query = select(cls.model).filter_by(**arg)
            result = await session.execute(query)
            return result.mappings().all()