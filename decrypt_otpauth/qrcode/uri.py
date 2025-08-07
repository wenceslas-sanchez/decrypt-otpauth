import base64
from typing import Protocol
from urllib.parse import quote, urlencode

from decrypt_otpauth.otpauth.types_ import Account


class UriGenerator(Protocol):
    """Protocol for generating OTP URIs."""

    def get_uri(self, *args, **kwargs) -> str:
        """Generate the complete OTP URI."""

    def get_uri_label(self, *args, **kwargs) -> str:
        """Generate the label part of the URI."""

    def get_uri_parameters(self, *args, **kwargs) -> str:
        """Generate the query parameters part of the URI."""


class OtpUriGenerator:
    """Standard OTP URI generator implementation."""

    def __init__(self, scheme: str = "otpauth"):
        self._scheme = scheme

    def get_uri(self, account: Account) -> str:
        uri_label = self.get_uri_label(account)
        uri_params = self.get_uri_parameters(account)
        return f"{self._scheme}://{account.type_.name_value}/{uri_label}?{uri_params}"

    def get_uri_label(self, account: Account) -> str:
        return quote(f"{account.issuer}:{account.label}")

    def get_uri_parameters(self, account: Account) -> str:
        parameters = {
            "secret": self._decode_secret(account.secret),
            "algorithm": account.algorithm.name_value,
            "period": account.period,
            "digits": account.digits,
            "issuer": account.issuer,
            "counter": account.counter,
        }
        return urlencode(parameters)

    @staticmethod
    def _decode_secret(secret: bytes) -> str:
        return base64.b32encode(secret).decode("utf-8").rstrip("=")
