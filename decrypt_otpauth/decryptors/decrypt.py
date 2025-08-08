import hashlib

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def decrypt_aes_cbc(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    if len(key) != 32:
        msg = "key must be 32 bytes for AES-256"
        raise ValueError(msg)
    if len(iv) != 16:
        msg = "IV must be 16 bytes"
        raise ValueError(msg)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    return _strip_pkcs7_padding(decryptor.update(ciphertext) + decryptor.finalize())


def generate_key(content: bytes, algorithm=hashlib.sha256) -> bytes:
    return algorithm(content).digest()


def _strip_pkcs7_padding(encrypted_data: bytes) -> bytes:
    if len(encrypted_data) == 0:
        return encrypted_data

    padding_length = encrypted_data[-1]
    if padding_length > 16 or padding_length == 0:
        return encrypted_data

    padding_suffix = encrypted_data[-padding_length:]
    if all(byte == padding_length for byte in padding_suffix):
        return encrypted_data[:-padding_length]
    return encrypted_data
