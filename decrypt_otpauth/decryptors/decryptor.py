from typing import Protocol


class Decryptor(Protocol):
    @classmethod
    def decrypt(cls, data: bytes, password: str) -> bytes:
        """Decrypt encrypted data using the provided password.

        Args:
            data: The encrypted data to decrypt
            password: The password used for decryption

        Returns:
            The decrypted data as bytes

        """
