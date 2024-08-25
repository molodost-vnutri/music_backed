from typing import Optional

from pydantic import BaseModel, PositiveInt

from source.exceptions import FilterEmptyException

class SUserMusic(BaseModel):
    id: PositiveInt
    name: str
    albom: Optional[str]
    artist: str

class SMusicFilter(SUserMusic):
    pass

class SFilterMusic:
    name: Optional[str]
    artist: Optional[str]
    albom: Optional[str]
    
    def __init__(self, name = None, artist = None, albom = None):
        if all(query is None for query in [name, artist, albom]):
            raise FilterEmptyException
        self.name = name
        self.artist = artist
        self.albom = albom