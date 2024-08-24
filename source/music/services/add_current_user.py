from pydantic import PositiveInt

from source.music.crud import MusicCRUD
from source.users.crud import UserMusicCRUD
from source.exceptions import MusicNotFoundException, MusicAlreadyAddException

async def add_current_music(user_id: PositiveInt, music_id: PositiveInt):
    music_exist = await MusicCRUD.model_find_one(id=music_id)
    if not music_exist:
        raise MusicNotFoundException
    music_user_exist = await UserMusicCRUD.model_find_one(user_id=user_id, music_id=music_id)
    if music_user_exist:
        raise MusicAlreadyAddException
    await UserMusicCRUD.model_insert(user_id=user_id, music_id=music_id)