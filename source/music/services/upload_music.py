from uuid import uuid4

from fastapi import UploadFile
from aiofiles import open

from source.Core import get_file_ext
from source.music.services.hashed import get_hash
from source.settings import music_folder
from source.music.crud import GenreCRUD, MusicCRUD, MusicEndCRUD
from source.exceptions import GenreNotFoundException, MusicAlreadyExistException, FileNotSupportedException

async def upload_music(name, albom, artist, genre, file: UploadFile):
    endfile = get_file_ext(file.filename)
    
    unique_name = uuid4()

    find = await MusicEndCRUD.model_find_one(file_end=endfile)

    if not find:
        raise FileNotSupportedException
    
    genre_obj = await GenreCRUD.model_find_one(genre=genre)
    if not genre_obj:
        raise GenreNotFoundException

    genre_id = genre_obj.id

    body = await file.read()

    hash = get_hash(body)

    is_exist = await MusicCRUD.model_find_one(hash=hash)

    if is_exist:
        raise MusicAlreadyExistException

    filename = f'{unique_name}.{endfile}'
    path = music_folder.joinpath(filename)

    async with open(path, mode='wb') as music_file:
        await music_file.write(body)

    await MusicCRUD.model_music_insert(name=name, albom=albom, artist=artist, path=filename, id_=genre_id, hash=hash)
