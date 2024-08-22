from typing import Optional

from fastapi import APIRouter, Depends, UploadFile, Form, File


from source.users.services.dependencies import get_current_user
from source.music.crud import MusicCRUD
from source.music.schemes import SFilterMusic

router = APIRouter(
    prefix='/music',
    tags=['Роуты для музыки']
)

@router.get('/current', status_code=200)
async def get_music_current_user_router(user_id = Depends(get_current_user)):
    return await MusicCRUD.model_get_music_current_user(model_id=user_id)

@router.get('/find', status_code=200)
async def find_music_router(query = Depends(SFilterMusic)):
    return query

@router.post('/upload', status_code=201)
async def upload_music_router(
    name: str = Form(...),
    albom: Optional[str] = Form(None),
    artist: str = Form(...),
    genre: str = Form(...),
    file: UploadFile = File(...),
    user_id=Depends(get_current_user)
):
    ...