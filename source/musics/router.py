from fastapi import APIRouter, Depends
from pydantic import PositiveInt

from source.users.services.dependencies import get_current_user
from source.musics.schemes import SFilterMusic
from source.musics.crud import MusicCRUD
from source.musics.services import add_music_current_user, get_music_by_id, get_music_file

router = APIRouter(
    prefix='/music',
    tags=['Роуты музыки']
)


@router.get('/find', status_code=200)
async def find_music_router(filter = Depends(SFilterMusic)):
    return await MusicCRUD.find_music_query(filter=filter)

@router.get('/add', status_code=200)
async def add_music_current_user_router(music_id: PositiveInt, user_id = Depends(get_current_user)):
    if not isinstance(user_id, int):
        return user_id
    return await add_music_current_user(music_id=music_id, user_id=user_id)


@router.get("/{music_id}", status_code=200)
async def get_music_by_id_router(music_id: PositiveInt):
    return await get_music_by_id(music_id=music_id)


@router.get("/{music_id}/file", status_code=200)
async def get_music_file_router(music_id: PositiveInt):
    return await get_music_file(music_id=music_id)