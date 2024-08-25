from uuid import uuid4
from typing import Optional
from hashlib import md5
from os import remove

from fastapi import UploadFile
from aiofiles import open
from pydantic import PositiveInt


from source.musics.crud import MusicCRUD, GenreCRUD
from source.settings import music_folder
from source.exceptions import FilterEmptyException, MusicAlreadyExistException, MusicNotFoundException, FileNotEndswithException, FileNotSupportedException, GenreNotFoundException

async def upload_music(name: str, albom: Optional[str], artist: str, genre: str, file: UploadFile):
    if not file.filename.count('.') or file.filename.endswith('.'):
        raise FileNotEndswithException
    endfile = file.filename.split('.')[1]
    if endfile not in ['mp3', 'wav']:
        raise FileNotSupportedException
    genre = await GenreCRUD.model_find_one(genre=genre)
    if not genre:
        raise GenreNotFoundException
    
    unique_name = uuid4()

    body = await file.read()

    hash = md5(body).hexdigest()

    if await MusicCRUD.model_find_one(hash=hash):
        raise MusicAlreadyExistException
    
    filename = '{}.{}'.format(unique_name, endfile)
    path = music_folder.joinpath(filename)

    try:
        async with open(path, mode='wb') as music_file:
            await music_file.write(body)
        music_id = await MusicCRUD.upload_music(name=name, albom=albom, artist=artist, hash=hash, genre_id=genre.id, path=path.__str__())
        return {
            'message': 'Музыка успешно добавлена id {}'.format(music_id)
        }
    except:
        if path.is_file():
            remove(path)
        raise MusicNotFoundException

async def delete_music(music_id: PositiveInt):
    path = await MusicCRUD.model_delete(music_id=music_id)
    file_path = music_folder.joinpath(path)
    if file_path.is_file():
        remove(file_path)
    return {
        'message': 'Музыка с id {} удалена'.format(music_id)
    }

async def update_music(music_id: PositiveInt, name: Optional[str], albom: Optional[str], artist: Optional[str], genre: Optional[str], file: Optional[UploadFile]):
    query_dict = {}
    if name:
        query_dict['name'] = name
    if albom:
        query_dict['albom'] = albom
    if artist:
        query_dict['artist'] = artist
    if not query_dict and not file:
        raise FilterEmptyException
    if file:
        if not file.filename.count('.') or file.filename.endswith('.'):
            raise FileNotEndswithException
        endfile = file.filename.split('.')[1]
        if endfile not in ['mp3', 'wav']:
            raise FileNotSupportedException
        result = await MusicCRUD.model_find_one(id=music_id)
        if not result:
            raise MusicNotFoundException
        file_path_old = music_folder.joinpath(result.path)
        
        unique_name = uuid4()

        filename = '{}.{}'.format(unique_name, endfile)
        file_path_new = music_folder.joinpath(filename)

        body = await file.read()

        hash = md5(body).hexdigest()

        query_dict['hash'] = hash
        query_dict['path'] = filename

        async with open(file_path_new, mode='wb') as music_file:
            await music_file.write(body)
        if file_path_old.is_file():
            remove(file_path_old)
    await MusicCRUD.update_music(model_id=music_id, genre=genre, **query_dict)
    return {
        'message': 'Музыка успешно обновлена'
    }