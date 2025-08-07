import enum
from typing import Any

from decrypt_otpauth.otpauth.reverse_enum import ReverseEnumMixin


class OneTimePasswordType(ReverseEnumMixin, enum.Enum):
    Unknown = 0
    HOTP = 1
    TOTP = 2

    @property
    def name_value(self):
        return self.name.lower()


class Algorithm(ReverseEnumMixin, enum.Enum):
    Unknown = 0
    SHA1 = 1
    SHA256 = 2
    SHA512 = 3
    MD5 = 4

    @property
    def name_value(self):
        if self == Algorithm.Unknown:
            return "sha1"
        return self.name.lower()


class Account:
    def __init__(
        self,
        secret: bytes,
        label: str,
        period: int,
        type_: int | OneTimePasswordType,
        issuer: str | None,
        digits: int,
        algorithm: int | Algorithm,
        counter: int,
        *args,
        **kwargs,
    ):
        self.secret = secret
        self.label = label
        self.period = period
        self.type_ = self._reverse_enum_from_value(type_, OneTimePasswordType)
        self.issuer = issuer
        self.digits = digits
        self.algorithm = self._reverse_enum_from_value(algorithm, Algorithm)
        self.counter = counter

    def to_dict(self) -> dict:
        return {
            "secret": self.secret,
            "label": self.label,
            "period": self.period,
            "type_": self.type_.name_value,
            "issuer": self.issuer,
            "digits": self.digits,
            "algorithm": self.algorithm.name_value,
            "counter": self.counter,
        }

    @staticmethod
    def _reverse_enum_from_value(
        value: Any, typ: type[ReverseEnumMixin]
    ) -> ReverseEnumMixin:
        if isinstance(value, str):
            return typ.from_reverse_key(value)
        return typ(value)


class Folder:
    def __init__(self, name: str, accounts: list[dict]):
        self.name = name
        self.accounts = [Account(**account) for account in accounts]

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "accounts": [account.to_dict() for account in self.accounts],
        }
