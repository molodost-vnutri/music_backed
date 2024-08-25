from fastapi import APIRouter, Depends

from source.users.services.dependencies import get_current_user
from source.musics.crud import MusicCRUD
from source.users.crud import UserCRUD
from source.users.schemes import SChangeFi, SChangeUsername, SUserChangeEmail
from source.users.user_information.services import change_email_first, change_email_last, change_email_second

router = APIRouter(
    prefix='/profile',
    tags=['Роутер работы с юзером']
)

@router.get('/information', status_code=200)
async def user_information_router(user_id = Depends(get_current_user)):
    if not isinstance(user_id, int):
        return user_id
    return await UserCRUD.get_info_current_user(model_id=user_id)


@router.patch('/update/username', status_code=200)
async def change_username_router(request: SChangeUsername, user_id = Depends(get_current_user)):
    if not isinstance(user_id, int):
        return user_id
    await UserCRUD.model_update(model_id=user_id, username=request.username)
    return {
        'message': 'Юзернейм успешно изменён на {}'.format(request.username)
    }


@router.patch('/update/fi', status_code=200)
async def change_fi_router(request: SChangeFi, user_id = Depends(get_current_user)):
    if not isinstance(user_id, int):
        return user_id
    await UserCRUD.model_update(model_id=user_id, first_name=request.first_name, last_name=request.last_name)
    return {
        'message': 'Фамилия и имя успешно изменены на {} {}'.format(request.first_name, request.last_name)
    }


@router.post('/change/email', status_code=200)
async def change_email_step_one_router(request: SUserChangeEmail, user_id = Depends(get_current_user)):
    if not isinstance(user_id, int):
        return user_id
    return await change_email_first(request=request, user_id=user_id)


@router.get('/change/email/second/{}', status_code=200)
async def change_email_step_two_router(token: str, user_id = Depends(get_current_user)):
    if not isinstance(user_id, int):
        return user_id
    return await change_email_second(token)


@router.get('/change/email/last/{}', status_code=200)
async def change_email_step_three_router(token: str, user_id = Depends(get_current_user)):
    if not isinstance(user_id, int):
        return user_id
    return await change_email_last(token=token, user_id=user_id)


@router.get('/musics', status_code=200)
async def get_user_musics_router(user_id = Depends(get_current_user)):
    if not isinstance(user_id, int):
        return user_id
    return await MusicCRUD.find_music_current_user(model_id=user_id)