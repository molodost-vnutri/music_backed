from typing import Optional

from pydantic import BaseModel


class SFilterMusic:
    name: str
    genre: Optional[str] = None
    artist: Optional[str] = None

    def __init__(self, name: str, genre: Optional[str] = None, artist: Optional[str] = None):
        self.name = name
        self.genre = genre
        self.artist = artist

class SMusicsList(BaseModel):
    name: str
    album: Optional[str] = None
    artist: str
    genre: str