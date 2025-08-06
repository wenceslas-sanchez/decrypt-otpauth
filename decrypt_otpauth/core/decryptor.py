from typing import Protocol


class Decryptor(Protocol):
    def decrypt(self, data: bytes, password: str) -> bytes:
        """Decrypt encrypted data using the provided password.

        Args:
            data: The encrypted data to decrypt
            password: The password used for decryption

        Returns:
            The decrypted data as bytes

        """
