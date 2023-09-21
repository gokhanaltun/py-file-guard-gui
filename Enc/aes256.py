from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from Enc import sha256 as sha
from Data.data import Data

backend = default_backend()


def encrypt(enc_key: bytes, data: bytes):
    try:
        data_hash = data[-32:]
        raw_data = data[:-32]

        if sha.check_hash(data_hash, raw_data):
            return Data(error="This file has already been encrypted.")

        iv = enc_key[-16:]

        cipher = Cipher(algorithms.AES(enc_key), modes.CBC(iv), backend=backend)
        encryptor = cipher.encryptor()

        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data) + padder.finalize()

        cipher_data = encryptor.update(padded_data) + encryptor.finalize()
        return Data(data=cipher_data + sha.hash_data(cipher_data))

    except Exception as e:
        return Data(error=e)


def decrypt(dec_key: bytes, encrypted_data: bytes):
    try:
        data_hash = encrypted_data[-32:]
        raw_data = encrypted_data[:-32]

        if not sha.check_hash(data_hash, raw_data):
            return Data(error="This file is not encrypted or has not been encrypted by this software. It cannot be decrypted.")

        iv = dec_key[-16:]

        cipher = Cipher(algorithms.AES(dec_key), modes.CBC(iv), backend=backend)
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(raw_data) + decryptor.finalize()

        unpadder = padding.PKCS7(128).unpadder()
        unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
        return Data(data=unpadded_data)

    except Exception as e:
        return Data(error=e)
