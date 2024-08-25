from source.exceptions import MusicNotFoundException, MusicAlreadyAddException

from pydantic import PositiveInt

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