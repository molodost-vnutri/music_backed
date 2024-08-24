from typing import List

from sqlalchemy import select, insert, text
from sqlalchemy.ext.asyncio import AsyncSession

from source.exceptions import RollbackException
from source.Core import BaseCRUD
from source.database import async_session
from source.music.models import MusicGenreModel, MusicModel, GenreModel, MusicEndModel
from source.music.schemes import SFilterMusic, SMusicsList
from source.SQL.music import GET_MUSIC_CURRENT_USER

class MusicCRUD(BaseCRUD):
    model = MusicModel

    @classmethod
    async def model_insert(cls, session: AsyncSession, **arg):
        query = insert(cls.model).values(**arg).returning(cls.model.id)
        result = await session.execute(query)
        return result.scalar_one()

    @classmethod
    async def model_get_music_current_user(cls, model_id: int):
        results: List[SMusicsList] = []
        async with async_session() as session:
            query = text(GET_MUSIC_CURRENT_USER)
            result = await session.execute(query, {'user_id': model_id})
            vector_results = result.fetchall()
            for result in vector_results:
                results.append(SMusicsList(name=result[0], album=result[1], artist=result[2], genre=result[3]))
            return results

    
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
    
    @classmethod
    async def filter_music(cls, request: SFilterMusic):
        FIND_QUERY = """
            SELECT m.id, m.name, m.albom, m.artist, STRING_AGG(g.genre, ', ') AS genres
            FROM musics m
            LEFT JOIN music_genres mg ON m.id = mg.music_id
            LEFT JOIN genres g ON mg.genre_id = g.id
            WHERE m.name ILIKE :name
        """

        if request.genre:
            FIND_QUERY += " AND g.genre = :genre"
        if request.artist:
            FIND_QUERY += " AND m.artist = :artist"

        FIND_QUERY += " GROUP BY m.id, m.name, m.albom, m.artist"

        async with async_session() as session:
            result = await session.execute(
                text(FIND_QUERY),
                {
                    'name': f'%{request.name}%',
                    'genre': request.genre,
                    'artist': request.artist
                }
            )

            result_list = [dict(row) for row in result.mappings()]

            return result_list

                    

class MusicGenreCRUD(BaseCRUD):
    model = MusicGenreModel

    @classmethod
    async def model_find_all(cls, **arg):
        async with async_session() as session:
            query = select(cls.model).filter_by(**arg)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def model_insert(cls, session: AsyncSession, **arg):
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