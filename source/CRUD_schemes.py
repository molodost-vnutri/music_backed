from source.users.schemes import SUserModeratorOut


class SUserPGOut(SUserModeratorOut):
    password: str
    
    class Config:
        from_atributes = True