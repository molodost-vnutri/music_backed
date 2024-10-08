from pathlib import Path
from typing import ClassVar


from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import EmailStr, PositiveInt

class Settings(BaseSettings):
    postgres_url: str
    secret_key: str
    algorithm: str
    smtp_host: str
    smtp_port: PositiveInt
    smtp_mail: EmailStr
    smtp_pass: str
    hostname: str

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(env_file='.env')

settings = Settings()

music_folder: Path = Path('music_folder')

if not music_folder.is_dir():
    music_folder.mkdir()