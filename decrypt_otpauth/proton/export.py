import enum
import json
import sys
import uuid
from typing import Any

from decrypt_otpauth.otpauth.types_ import Account, Folder, OneTimePasswordType
from decrypt_otpauth.qrcode.uri import OtpUriGenerator

PROTON_EXPORT_VERSION = 1


class FolderPlacement(enum.Enum):
    """Where to keep the OTP Auth folder name, since Proton Authenticator has no folders."""

    NOTE = "note"
    PREFIX = "prefix"


class ProtonExporter:
    """Builds a Proton Authenticator import file from OTP Auth folders."""

    def __init__(
        self,
        uri_generator: OtpUriGenerator | None = None,
        folder_placement: FolderPlacement = FolderPlacement.NOTE,
    ):
        self.uri_generator = uri_generator or OtpUriGenerator()
        self.folder_placement = folder_placement

    def build_export(self, folders: dict[str, Folder]) -> dict[str, Any]:
        entries = []
        for folder_name, folder in folders.items():
            for account in folder.accounts:
                # Proton Authenticator only supports time-based codes
                if account.type_ != OneTimePasswordType.TOTP:
                    print(
                        f"Skipping account {account.label} ({account.issuer}): "
                        f"unsupported type {account.type_.name}",
                        file=sys.stderr,
                    )
                    continue
                entries.append(self._build_entry(account, folder_name))
        return {"version": PROTON_EXPORT_VERSION, "entries": entries}

    def export(self, folders: dict[str, Folder], output_path: str) -> None:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.build_export(folders), f, indent=2, ensure_ascii=False)
            f.write("\n")

    def _build_entry(self, account: Account, folder_name: str) -> dict[str, Any]:
        name = account.label
        note = None
        if folder_name:
            if self.folder_placement == FolderPlacement.PREFIX:
                name = f"{folder_name} - {name}"
            else:
                note = folder_name
        return {
            "id": str(uuid.uuid4()),
            "content": {
                "uri": self.uri_generator.get_uri(account),
                "entry_type": "Totp",
                "name": name,
            },
            "note": note,
        }
