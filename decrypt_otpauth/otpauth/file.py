from decrypt_otpauth.core.file import read_file
from decrypt_otpauth.decryptors.decrypt import (
    generate_key,
    decrypt_aes_cbc,
)


def read_otpauth(path: str) -> bytes:
    iv = bytes(16)
    key = generate_key("Authenticator".encode("utf-8"))
    return decrypt_aes_cbc(read_file(path), key, iv)
