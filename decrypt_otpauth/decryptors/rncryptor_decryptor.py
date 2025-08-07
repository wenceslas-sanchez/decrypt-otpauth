import hashlib
import hmac
from dataclasses import dataclass

from decrypt_otpauth.decryptors.decrypt import decrypt_aes_cbc
from decrypt_otpauth.decryptors.decryptor import Decryptor


@dataclass
class RNCryptorComponents:
    """Data structure for parsed RNCryptor components"""

    version: int
    options: int
    encryption_salt: bytes
    hmac_salt: bytes
    iv: bytes
    ciphertext: bytes
    hmac_value: bytes
    header_and_ciphertext: bytes

    __MIN_DATA_SIZE = (
        66  # version(1) + options(1) + enc_salt(8) + hmac_salt(8) + iv(16) + hmac(32)
    )
    __SUPPORTED_VERSION = 3

    @classmethod
    def from_bytes(cls, data: bytes) -> "RNCryptorComponents":
        """Parse RNCryptor data into components"""
        cls._validate_data(data)
        return cls(
            version=data[0],
            options=data[1],
            encryption_salt=data[2:10],
            hmac_salt=data[10:18],
            iv=data[18:34],
            ciphertext=data[34:-32],
            hmac_value=data[-32:],
            header_and_ciphertext=data[:-32],
        )

    @classmethod
    def _validate_data(cls, data: bytes) -> None:
        if len(data) < cls.__MIN_DATA_SIZE:
            msg = f"data too short for RNCryptor format (minimum {cls.__MIN_DATA_SIZE} bytes)"
            raise ValueError(msg)
        if data[0] != cls.__SUPPORTED_VERSION:
            msg = f"Unsupported RNCryptor version: {data[0]}"
            raise ValueError(msg)


class RNCryptorDecryptor(Decryptor):
    """Decryptor for RNCryptor format"""

    SALT_SIZE = 8
    IV_SIZE = 16
    HMAC_SIZE = 32
    KEY_SIZE = 32
    PBKDF2_ITERATIONS = 10000

    @classmethod
    def decrypt(cls, data: bytes, password: str) -> bytes:
        """Main decryption method"""
        password_bytes = password.encode("utf-8")

        components = RNCryptorComponents.from_bytes(data)
        cls._check_hmac(components, password_bytes)

        encryption_key = cls._derive_key(password_bytes, components.encryption_salt)
        return decrypt_aes_cbc(components.ciphertext, encryption_key, components.iv)

    @classmethod
    def _derive_key(cls, password_bytes: bytes, salt: bytes) -> bytes:
        return hashlib.pbkdf2_hmac(
            "sha1",
            password_bytes,
            salt,
            cls.PBKDF2_ITERATIONS,
            cls.KEY_SIZE,
        )

    @classmethod
    def _check_hmac(
        cls, components: RNCryptorComponents, password_bytes: bytes
    ) -> None:
        hmac_key = cls._derive_key(password_bytes, components.hmac_salt)
        expected_hmac = hmac.new(
            hmac_key, components.header_and_ciphertext, hashlib.sha256
        ).digest()

        if hmac.compare_digest(components.hmac_value, expected_hmac):
            return
        msg = "HMAC verification failed - wrong password or corrupted data"
        raise ValueError(msg)
