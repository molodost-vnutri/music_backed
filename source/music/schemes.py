from typing import Optional


class SFilterMusic:
    name: str
    genre: Optional[str]
    artist: Optional[str]

    def __init__(self, name: str, genre: Optional[str] = None, artist: Optional[str] = None):
        self.name = name
        self.genre = genre
        self.artist = artist
