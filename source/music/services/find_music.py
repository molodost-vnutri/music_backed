from source.music.crud import MusicCRUD
from source.music.schemes import SFilterMusic
async def find(request: SFilterMusic):
    return await MusicCRUD.filter_music(request=request)