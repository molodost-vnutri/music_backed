from uuid import uuid4

from fastapi import UploadFile

from source.Core import invert_dict, get_file_ext
from source.settings import music_folder
from source.music.crud import MusicCRUD, MusicEndCRUD
from source.exceptions import MusicAlreadyExistException, FileNotSupportedException

async def upload_music(name, albom, artist, genre, file: UploadFile):
    endfile = get_file_ext(file.filename)
    
    unique_name = uuid4()

    results = await MusicEndCRUD.model_find_all()

    dict_end: dict = {}

    for result in results:
        dict_end[result['MusicEndModel'].id] = result['MusicEndModel'].file_end
    invert_endfiles = invert_dict(dict_end)

    if not invert_endfiles.get(endfile):
        raise FileNotSupportedException
    
    filename = '{}.{}'.format(unique_name, endfile)

    path = music_folder.joinpath(filename)

    body = await file.read()

    with open(path, mode='wb') as music_file:
        music_file.write(body)

    await MusicCRUD.model_music_insert(name=name, albom=albom, artist=artist, genre=genre, path=filename)