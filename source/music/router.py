from typing import Optional

from fastapi import APIRouter, Depends, UploadFile, Form, File


from source.users.services.dependencies import get_current_user, check_current_admin
from source.music.crud import MusicCRUD
from source.music.schemes import SFilterMusic
from source.music.services.upload_music import upload_music

router = APIRouter(
    prefix='/music',
    tags=['Роуты для музыки']
)

@router.get('/current', status_code=200)
async def get_music_current_user_router(user_id = Depends(get_current_user)):
    return await MusicCRUD.model_get_music_current_user(model_id=user_id)

@router.get('/find', status_code=200)
async def find_music_router(query = Depends(SFilterMusic)):
    return await MusicCRUD.model_find_all(
        name=query.name,
    )

@router.post('/_/upload', status_code=201)
async def upload_music_router(
    name: str = Form(...),
    albom: Optional[str] = Form(None),
    artist: str = Form(...),
    genre: str = Form(...),
    file: UploadFile = File(...),
    _=Depends(check_current_admin)
):
    await upload_music(name=name.lower(), albom=albom.lower(), artist=artist.lower(), genre=genre.lower(), file=file)
    return {
        'message': 'Музыка успешно загружена'
    }