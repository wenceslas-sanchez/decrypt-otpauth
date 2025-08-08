import getpass

from decrypt_otpauth.decryptors.rncryptor_decryptor import RNCryptorDecryptor
from decrypt_otpauth.ns_keyed_unarchiver.unarchiver import NSKeyedUnarchiver
from decrypt_otpauth.otpauth.file import read_otpauth
from decrypt_otpauth.otpauth.ns_types import NSAccount, NSFolder
from decrypt_otpauth.otpauth.types_ import Folder
from decrypt_otpauth.parse_args import parse_args
from decrypt_otpauth.qrcode.qrcode import fetch_and_display
from decrypt_otpauth.qrcode.uri import OtpUriGenerator


def main():
    args = parse_args()
    otpauth_archive = read_otpauth(args.path)

    otpauth_unarchive = NSKeyedUnarchiver(otpauth_archive).unarchive()
    password = getpass.getpass(f'Password for export file {args.path}: ')
    otpauth_data_decrypted_archive = RNCryptorDecryptor.decrypt(otpauth_unarchive["WrappedData"], password)

    ns_unarchiver = NSKeyedUnarchiver(otpauth_data_decrypted_archive)
    ns_unarchiver.register_type(NSFolder)
    ns_unarchiver.register_type(NSAccount)
    otpauth_data_decrypted_unarchive = ns_unarchiver.unarchive()

    folders = {}
    for otp_folder in otpauth_data_decrypted_unarchive["Folders"]:
        folder = Folder(**otp_folder)
        folders[folder.name] = folder

    for folder_name, folder in folders.items():
        print(f"\nFolder '{folder_name}'")
        for account in folder.accounts:
            print(f"\nAccount {account.label}:\n")
            uri = OtpUriGenerator().get_uri(account)
            fetch_and_display(uri)
            input("Press Enter to continue...")


if __name__ == '__main__':
    main()
