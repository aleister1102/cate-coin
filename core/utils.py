import hashlib

def hash(data) -> str:
    data = data.encode('utf-8')
    return hashlib.sha256(data).hexdigest()
