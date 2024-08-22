from sqlalchemy import select

from source.Core import BaseCRUD
from source.database import async_session
from source.music.models import MusicGenreModel, MusicModel, GenreModel

class MusicCRUD(BaseCRUD):
    model = MusicModel

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


class MusicGenreCRUD(BaseCRUD):
    model = MusicGenreModel

class GenreCRUD(BaseCRUD):
    model = GenreModel