import enum
import inspect
from decrypt_otpauth.otpauth.algorithm import Algorithm


class AccountType(enum.Enum):
    Unknown = 0
    HOTP = 1
    TOTP = 2

    @property
    def uri_value(self):
        return self.name.lower()


class Account:
    def __init__(
        self,
        secret: bytes,
        label: str,
        period: int,
        type: int,
        issuer: str | None,
        digits: int,
        algorithm: int,
        counter: int,
        *args,
        **kwargs,
    ):
        self.secret = secret
        self.label = label
        self.period = period
        self.type = AccountType(type)
        self.issuer = issuer
        self.digits = digits
        self.algorithm = Algorithm(algorithm)
        self.counter = counter

    @classmethod
    def from_dict(cls, dct: dict) -> "Account":
        return cls(
            **{k: v for k, v in dct.items() if k in inspect.signature(cls).parameters}
        )
