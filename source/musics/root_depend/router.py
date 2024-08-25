from typing import Optional

from fastapi import APIRouter, Depends, Form, UploadFile, File
from pydantic import PositiveInt

from source.users.services.dependencies import check_current_depend
from source.musics.root_depend.services import upload_music, delete_music, update_music
from source.musics.crud import MusicCRUD, GenreCRUD


router = APIRouter(
    prefix='/_/music',
    tags=["Роуты для crud'a музыки"]
)

@router.get('/all', status_code=200)
async def get_all_music_router(_ = Depends(check_current_depend)):
    return await MusicCRUD.get_all()


@router.post('/_/upload', status_code=201)
async def upload_music_router(
    name: str = Form(...),
    albom: Optional[str] = Form(None),
    artist: str = Form(...),
    genre: str = Form(...),
    file: UploadFile = File(...),
    _=Depends(check_current_depend)
):
    return await upload_music(name=name.lower(), albom=albom, artist=artist.lower(), genre=genre.lower(), file=file)


@router.post('/_/add_genre', status_code=201)
async def add_genre_router(genre: str = Form(...), _ = Depends(check_current_depend)):
    await GenreCRUD.model_insert(genre=genre.lower())
    return {
        'message': 'Жанр добавлен'
    }

@router.delete('/_/delete/music', status_code=200)
async def delete_music_router(music_id: PositiveInt, _ = Depends(check_current_depend)):
    return await delete_music(music_id=music_id)


@router.put('/_/update/music', status_code=200)
async def update_music_router(
    music_id: PositiveInt = Form(...),
    name: Optional[str] = Form(None),
    albom: Optional[str] = Form(None),
    artist: Optional[str] = Form(None),
    genre: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    _ = Depends(check_current_depend)
):
    return await update_music(music_id=music_id, name=name, albom=albom, artist=artist, genre=genre, file=file)