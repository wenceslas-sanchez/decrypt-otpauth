import enum
from decrypt_otpauth.otpauth.algorithm import Algorithm
from decrypt_otpauth.ns_keyed_unarchiver.types_ import NSType, Unarchiver


class OtpAccountType(enum.Enum):
    Unknown = 0
    HOTP = 1
    TOTP = 2

    @property
    def uri_value(self):
        return self.name.lower()


class OtpAccount(NSType):
    """Handler for Account objects from NSKeyedArchiver"""

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
        self.type = OtpAccountType(type)
        self.issuer = issuer
        self.digits = digits
        self.algorithm = Algorithm(algorithm)
        self.counter = counter

    @classmethod
    def class_names(cls) -> list[str]:
        return ["ACOTPAccount"]

    @classmethod
    def unarchive(cls, obj: dict, unarchiver: Unarchiver) -> dict:
        """
        Unarchive an Account object from NSKeyedArchiver format.

        Args:
            obj: The raw object dictionary from NSKeyedArchiver
            unarchiver: Reference to the unarchiver for resolving references

        Returns:
            The unarchived Account object
        """
        resolved_obj = unarchiver._resolve_refs_in_dict(obj)
        account_data = {
            "secret": resolved_obj.get("secret", b""),
            "label": resolved_obj.get("label", ""),
            "period": resolved_obj.get("period", 30),
            "type": resolved_obj.get("type", 0),
            "issuer": resolved_obj.get("issuer"),
            "digits": resolved_obj.get("digits", 6),
            "algorithm": resolved_obj.get("algorithm", 1),
            "counter": resolved_obj.get("counter", 0),
        }

        return cls(**account_data).to_dict()

    def to_dict(self) -> dict:
        """Convert OTPAccount to dictionary representation"""
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


class OtpFolder(NSType):
    """Handler for OTPFolder objects from NSKeyedArchiver"""

    def __init__(self, name: str, accounts):
        self.name = name
        self.accounts = accounts or []

    @classmethod
    def class_names(cls) -> list[str]:
        """Return list of Objective-C class names this type handles"""
        return ["ACOTPFolder"]

    @classmethod
    def unarchive(cls, obj: dict, unarchiver: Unarchiver) -> dict:
        """
        Unarchive an OTPFolder object from NSKeyedArchiver format.

        Args:
            obj: The raw object dictionary from NSKeyedArchiver
            unarchiver: Reference to the unarchiver for resolving references

        Returns:
            The unarchived OTPFolder object
        """
        # Resolve any UID references in the object dictionary
        resolved_obj = unarchiver._resolve_refs_in_dict(obj)

        name = resolved_obj.get("name", "")
        if isinstance(name, dict) and "$class" in name:
            name = unarchiver._resolve_ref(name)

        accounts = resolved_obj.get("accounts", [])
        if isinstance(accounts, dict) and "$class" in accounts:
            accounts = unarchiver._resolve_ref(accounts)
        elif isinstance(accounts, list):
            accounts = [
                unarchiver._resolve_ref(account_ref) for account_ref in accounts
            ]

        return cls(name=name, accounts=accounts).to_dict()

    def to_dict(self) -> dict:
        """Convert OTPFolder to dictionary representation"""
        return {
            "name": self.name,
            "accounts": [
                account.to_dict() if hasattr(account, "to_dict") else account
                for account in self.accounts
            ],
        }

    def __getitem__(self, index):
        return self.accounts[index]
