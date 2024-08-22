from fastapi import FastAPI

from source.users.router import router as user_router
from source.music.router import router as music_router

application = FastAPI(
    title='Музыкальный сервис'
)

application.include_router(user_router)
application.include_router(music_router)