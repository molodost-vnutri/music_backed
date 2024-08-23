from hashlib import md5

def get_hash(body) -> str:
    return md5(body).hexdigest()