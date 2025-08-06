import hashlib
import hmac
from dataclasses import dataclass

from decrypt_otpauth.core.decrypt import decrypt_aes_cbc


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


class RNCryptorDecryptor:
    """Decryptor for RNCryptor format using hashlib and cryptography"""

    SALT_SIZE = 8
    IV_SIZE = 16
    HMAC_SIZE = 32
    KEY_SIZE = 32
    PBKDF2_ITERATIONS = 10000

    def decrypt(self, data: bytes, password: str) -> bytes:
        """Main decryption method"""

        components = RNCryptorComponents.from_bytes(data)
        keys = self._derive_keys(password.encode("utf-8"), components)
        self._check_hmac(components, keys["hmac_key"])

        return decrypt_aes_cbc(
            components.ciphertext, keys["encryption_key"], components.iv
        )

    def _derive_keys(
        self, password_bytes: bytes, components: RNCryptorComponents
    ) -> dict:
        return {
            "encryption_key": hashlib.pbkdf2_hmac(
                "sha1",
                password_bytes,
                components.encryption_salt,
                self.PBKDF2_ITERATIONS,
                self.KEY_SIZE,
            ),
            "hmac_key": hashlib.pbkdf2_hmac(
                "sha1",
                password_bytes,
                components.hmac_salt,
                self.PBKDF2_ITERATIONS,
                self.KEY_SIZE,
            ),
        }

    @staticmethod
    def _check_hmac(components: RNCryptorComponents, hmac_key: bytes) -> None:
        expected_hmac = hmac.new(
            hmac_key, components.header_and_ciphertext, hashlib.sha256
        ).digest()

        if hmac.compare_digest(components.hmac_value, expected_hmac):
            return
        msg = "HMAC verification failed - wrong password or corrupted data"
        raise ValueError(msg)
