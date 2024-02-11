import hashlib


def generate_hash(text):
    return hashlib.blake2b(str(text).encode('utf-8'), digest_size=16).hexdigest()
