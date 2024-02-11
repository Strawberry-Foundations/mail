import hashlib


def generate_hash(text):
    return hashlib.sha256(str(text).encode('utf-8')).hexdigest()
