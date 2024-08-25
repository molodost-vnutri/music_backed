from typing import Optional

from sqlalchemy import text, update
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import PositiveInt

from source.exceptions import MusicNotFoundException, GenreNotFoundException
from source.database import async_session
from source.Core import BaseCRUD
from source.musics.models import MusicModel, GenreModel
from source.musics.schemes import SUserMusic, SFilterMusic, SMusicFilter

class GenreCRUD(BaseCRUD):
    model = GenreModel

class MusicCRUD(BaseCRUD):
    model = MusicModel

    @staticmethod
    async def get_all():
        async with async_session() as session:
            query = text("""
                SELECT m.id, m.name, m.albom, m.artist, m.path, m.hash, g.genre
                FROM musics m
                LEFT JOIN music_genres mg ON m.id = mg.music_id
                LEFT JOIN genres g ON mg.genre_id = g.id
            """)
            result = await session.execute(query)
            rows = result.fetchall()

            data = [{
                'id': row[0],
                'name': row[1],
                'albom': row[2],
                'artist': row[3],
                'path': row[4],
                'hash': row[5],
                'genre': row[6]
            } for row in rows]
            return data
    
    @classmethod
    async def upload_music(cls, name: str, albom: Optional[str], artist: str, path: str, hash: str, genre_id: int):
        async with async_session() as session:
            async with session.begin():
                music_id = await cls.model_insert(session, name, albom, artist, path, hash)
                query = text("""
                    INSERT INTO music_genres (music_id, genre_id)
                    VALUES (:music_id, :genre_id)
                """)
                await session.execute(query, {'music_id': music_id, 'genre_id': genre_id})
                await session.commit()
                return music_id

    @staticmethod
    async def model_insert(session: AsyncSession, name: str, albom: Optional[str], artist: str, path: str, hash: str):
        query = text("""
            INSERT INTO musics (name, albom, artist, path, hash)
            VALUES (:name, :albom, :artist, :path, :hash)
            RETURNING id
        """)
        result = await session.execute(query, {
            'name': name,
            'albom': albom,
            'artist': artist,
            'path': path,
            'hash': hash
        })
        return result.scalar_one()
    
    @staticmethod
    async def find_music_current_user(model_id: PositiveInt):
        async with async_session() as session:
            query = text("""
                SELECT m.id, m.name, m.albom, m.artist
                FROM user_musics um
                JOIN musics m ON um.music_id = m.id
                WHERE um.user_id = :user_id
            """)
            result = await session.execute(query, {'user_id': model_id})
            rows = result.fetchall()
            user_music_list = [SUserMusic(id=row[0], name=row[1], albom=row[2], artist=row[3]) for row in rows]
            return user_music_list
    
    @staticmethod
    async def find_music_query(filter: SFilterMusic):
        async with async_session() as session:
            query = """
                SELECT m.id, m.name, m.albom, m.artist, g.genre
                FROM musics m
                LEFT JOIN music_genres mg ON m.id = mg.music_id
                LEFT JOIN genres g ON mg.genre_id = g.id
                WHERE 1=1;

            """
            if filter.name:
                query += " AND m.name LIKE :name"
            if filter.artist:
                query += " AND m.artist LIKE :artist"
            if filter.albom:
                query += " AND m.albom LIKE :albom"
            stmt = text(query)
            params = {}
            if filter.name:
                params['name'] = f"%{filter.name}%"
            if filter.artist:
                params['artist'] = f"%{filter.artist}%"
            if filter.albom:
                params['albom'] = f"%{filter.albom}%"
            result = await session.execute(stmt, params)
            musics = result.fetchall()
            music_list = [SMusicFilter(id=row[0], name=row[1], albom=row[2], artist=row[3])
                  for row in musics]
            return music_list
    
    @staticmethod
    async def find_exist_musics_current_user(model_id: PositiveInt, music_id: PositiveInt):
        async with async_session() as session:
            query = text('''
                SELECT user_id, music_id
                FROM user_musics
                WHERE user_id = :user_id
                AND music_id = :music_id
            ''')
            result = await session.execute(query, {'user_id': model_id, 'music_id': music_id})
            return result.scalars().all()
    
    @staticmethod
    async def add_music_current_user(model_id: PositiveInt, music_id: PositiveInt):
        async with async_session() as session:
            query = text('''
                INSERT INTO user_musics (user_id, music_id)
                VALUES (:user_id, :music_id)
            ''')
            await session.execute(query, {'user_id': model_id, 'music_id': music_id})
            await session.commit()
    
    @staticmethod
    async def model_delete(music_id: PositiveInt):
        async with async_session() as session:
            query_find = text('''
                SELECT id
                FROM musics
            ''')
            result = await session.execute(query_find)
            if not result.scalar_one_or_none():
                raise MusicNotFoundException
            query_delete = text('''
                WITH deleted_user_musics AS (
                    DELETE FROM user_musics WHERE music_id = :music_id
                ),
                deleted_music_genres AS (
                    DELETE FROM music_genres WHERE music_id = :music_id
                )
                DELETE FROM musics 
                WHERE id = :music_id
                RETURNING path
            ''')
            result = await session.execute(query_delete, {'music_id': music_id})
            await session.commit()
            return result.scalar_one()
    
    @classmethod
    async def model_update(cls, session: AsyncSession, model_id: PositiveInt, **arg):
        query = update(cls.model).filter_by(id=model_id).values(**arg).returning(cls.model)
        result = await session.execute(query)
        return result.scalar_one()
    
    @classmethod
    async def update_music(cls, model_id: PositiveInt, genre: Optional[str], **arg):
        async with async_session() as session:
            async with session.begin():
                if genre:
                    query = text('''
                        SELECT id, genre
                        FROM genres
                        WHERE genre = :genre
                    ''')
                    result = await session.execute(query, {'genre': genre})
                    genre = result.fetchall()
                    if not genre:
                        raise GenreNotFoundException
                    query = text('''
                        UPDATE music_genres
                        SET genre = :genre
                        WHERE id = :genre_id
                    ''')
                    session.execute(query, {'genre': genre[0], 'genre_id': genre[1]})
                await cls.model_update(session=session, model_id=model_id, **arg)
                await session.commit()
    
    @staticmethod
    async def get_music_by_id(model_id: PositiveInt):
        async with async_session() as session:
            query = text('''
                SELECT m.id, m.name, m.albom, m.artist, m.path, g.genre
                FROM musics m
                LEFT JOIN music_genres mg ON m.id = mg.music_id
                LEFT JOIN genres g ON mg.genre_id = g.id
                WHERE m.id = :model_id;
            ''')
            row = await session.execute(query, {'model_id': model_id})
            return row.fetchall()[0]