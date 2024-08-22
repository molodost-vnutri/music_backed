from passlib.context import CryptContext

pass_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hashed_password(password: str) -> str:
    return pass_context.hash(password)

def verify_password(password: str, hash: str) -> bool:
    return pass_context.verify(secret=password, hash=hash)