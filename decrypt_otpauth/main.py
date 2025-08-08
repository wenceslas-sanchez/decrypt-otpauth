import getpass
from typing import Any

from decrypt_otpauth.decryptors.rncryptor_decryptor import RNCryptorDecryptor
from decrypt_otpauth.ns_keyed_unarchiver.unarchiver import NSKeyedUnarchiver
from decrypt_otpauth.otpauth.file import read_otpauth
from decrypt_otpauth.otpauth.ns_types import NSAccount, NSFolder
from decrypt_otpauth.otpauth.types_ import Folder, Account
from decrypt_otpauth.parse_args import parse_args
from decrypt_otpauth.qrcode.qrcode import fetch_and_display
from decrypt_otpauth.qrcode.uri import OtpUriGenerator


class OTPAuthProcessor:
    """Handles the decryption and processing of OTPAuth export files."""

    def __init__(self):
        self.uri_generator = OtpUriGenerator()

    @staticmethod
    def _load_and_unarchive(file_path: str) -> dict[str, Any]:
        archive = read_otpauth(file_path)
        return NSKeyedUnarchiver(archive).unarchive()

    @staticmethod
    def _get_password(file_path: str) -> str:
        return getpass.getpass(f"Password for export file {file_path}: ")

    @staticmethod
    def _decrypt_data(unarchived_data: dict[str, Any], password: str) -> bytes:
        return RNCryptorDecryptor.decrypt(unarchived_data["WrappedData"], password)

    @staticmethod
    def _unarchive_decrypted_data(decrypted_data: bytes) -> dict[str, Any]:
        unarchiver = NSKeyedUnarchiver(decrypted_data)
        unarchiver.register_type(NSFolder)
        unarchiver.register_type(NSAccount)
        return unarchiver.unarchive()

    @staticmethod
    def _build_folder_structure(unarchived_data: dict[str, Any]) -> dict[str, Folder]:
        folders = {}
        for otp_folder in unarchived_data["Folders"]:
            folder = Folder(**otp_folder)
            folders[folder.name] = folder
        return folders

    def _display_account(self, account: Account) -> None:
        print(f"\nAccount {account.label}:\n")
        uri = self.uri_generator.get_uri(account)
        fetch_and_display(uri)
        input("Press Enter to continue...")

    def display_all_accounts(self, folders: dict[str, Folder]) -> None:
        """Display all accounts organized by folders."""
        for folder_name, folder in folders.items():
            print(f"\nFolder '{folder_name}'")
            for account in folder.accounts:
                self._display_account(account)

    def process_file(self, file_path: str) -> dict[str, Folder]:
        """Complete processing pipeline for an OTPAuth file."""
        unarchived = self._load_and_unarchive(file_path)
        password = self._get_password(file_path)
        decrypted_data = self._decrypt_data(unarchived, password)
        final_data = self._unarchive_decrypted_data(decrypted_data)
        return self._build_folder_structure(final_data)


def main() -> None:
    """Main entry point for the OTPAuth decryption tool."""
    args = parse_args()
    processor = OTPAuthProcessor()

    try:
        folders = processor.process_file(args.path)
        processor.display_all_accounts(folders)
    except Exception as e:
        print(f"Error processing file: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
