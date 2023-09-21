from cryptography.hazmat.primitives import hashes


def hash_data(data: bytes):
    hash_object = hashes.Hash(hashes.SHA256())
    hash_object.update(data)
    hashed_data = hash_object.finalize()
    return hashed_data


def check_hash(data_hash: bytes, data: bytes):
    hashed_data = hash_data(data)
    if hashed_data == data_hash:
        return True
    else:
        return False
