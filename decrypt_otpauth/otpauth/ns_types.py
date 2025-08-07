import enum
from decrypt_otpauth.otpauth.types_ import Account, Folder
from decrypt_otpauth.ns_keyed_unarchiver.types_ import NSType, Unarchiver


class OneTimePasswordType(enum.Enum):
    Unknown = 0
    HOTP = 1
    TOTP = 2

    @property
    def uri_value(self):
        return self.name.lower()


class OtpAccount(NSType):
    """Handler for Account objects from NSKeyedArchiver"""

    @classmethod
    def class_names(cls) -> list[str]:
        return ["ACOTPAccount"]

    @classmethod
    def unarchive(cls, obj: dict, unarchiver: Unarchiver) -> dict:
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

        return Account(**account_data).to_dict()


class OtpFolder(NSType):
    """Handler for OTPFolder objects from NSKeyedArchiver"""

    @classmethod
    def class_names(cls) -> list[str]:
        return ["ACOTPFolder"]

    @classmethod
    def unarchive(cls, obj: dict, unarchiver: Unarchiver) -> dict:
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

        return Folder(name, accounts).to_dict()
