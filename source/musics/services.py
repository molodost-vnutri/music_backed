from fastapi.responses import StreamingResponse
from aiofiles import open
from pydantic import PositiveInt

from source.musics.schemes import SMusicOut
from source.exceptions import MusicNotFoundException, MusicAlreadyAddException
from source.musics.crud import MusicCRUD

async def add_music_current_user(music_id: PositiveInt, user_id: PositiveInt):
    music_exist = await MusicCRUD.model_find_one(id=music_id)
    if not music_exist:
        raise MusicNotFoundException
    user_music_exist =  await MusicCRUD.find_exist_musics_current_user(model_id=user_id, music_id=music_id)
    if user_music_exist:
        raise MusicAlreadyAddException
    await MusicCRUD.add_music_current_user(model_id=user_id, music_id=music_id)
    return {
        'message': 'Музыка успешно добавлена на аккаунт'
    }


async def get_music_by_id(music_id: int):
    music_row = await MusicCRUD.get_music_by_id(model_id=music_id)
    if not music_row:
        raise MusicNotFoundException
    
    return {
        'information': {
            'name': music_row[1],
            'albom': music_row[2],
            'artist': music_row[3],
            'genre': music_row[5]
        },
        'file_url': f"/music/{music_id}/file"
    }


async def get_music_file(music_id: int):
    music_row = await MusicCRUD.get_music_by_id(model_id=music_id)
    if not music_row:
        raise MusicNotFoundException
    
    file_path = music_row[4]
    async def file_iterator():
        async with open(file_path, mode='rb') as music_body:
            while chunk := await music_body.read(1024):
                yield chunk

    return StreamingResponse(
        file_iterator(),
        media_type="audio/mpeg",
        headers={"Content-Disposition": f"attachment; filename={music_row[4]}"}
    )