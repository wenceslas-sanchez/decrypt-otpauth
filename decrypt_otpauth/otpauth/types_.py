import enum

from decrypt_otpauth.otpauth.algorithm import Algorithm


class OneTimePasswordType(enum.Enum):
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
        self.type = OneTimePasswordType(type)
        self.issuer = issuer
        self.digits = digits
        self.algorithm = Algorithm(algorithm)
        self.counter = counter

    def to_dict(self) -> dict:
        return {
            "secret": self.secret,
            "label": self.label,
            "period": self.period,
            "type": self.type.uri_value,
            "issuer": self.issuer,
            "digits": self.digits,
            "algorithm": self.algorithm.uri_string,
            "counter": self.counter,
        }


class Folder:
    def __init__(self, name: str, accounts: list[Account]):
        self.name = name
        self.accounts = accounts or []

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "accounts": [
                account.to_dict() for account in self.accounts
            ],
        }
