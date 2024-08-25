from fastapi import FastAPI

from source.users.create.router import router as create_user_router
from source.users.auth_user.router import router as auth_user_router
from source.users.user_information.router import router as user_router
from source.users.moderation.router import router as moderation_router
from source.musics.root_depend.router import router as depend_music_router
from source.musics.router import router as music_router

application = FastAPI(
    title='Музыкальный сервис'
)

application.include_router(create_user_router)
application.include_router(auth_user_router)
application.include_router(user_router)
application.include_router(depend_music_router)
application.include_router(moderation_router)
application.include_router(music_router)