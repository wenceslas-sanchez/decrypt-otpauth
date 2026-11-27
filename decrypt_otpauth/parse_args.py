import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="TODO")
    parser.add_argument(
        "-p",
        "--path",
        action="store",
        type=str,
        required=True,
        help="path to your encrypted OTP Auth backup (.otpauthdb)",
    )
    parser.add_argument(
        "--images-location",
        action="store",
        type=str,
        required=False,
        help="directory path to save QR code images instead of displaying them in terminal",
    )
    parser.add_argument(
        "--export-uris",
        action="store",
        type=str,
        required=False,
        metavar="FILE",
        help="export all otpauth:// URIs as plain text to FILE (one per line)",
    )
    parser.add_argument(
        "--export-proton",
        action="store",
        type=str,
        required=False,
        metavar="FILE",
        help="export all accounts as a Proton Authenticator JSON import file to FILE",
    )
    parser.add_argument(
        "--proton-folder-as",
        action="store",
        type=str,
        choices=["note", "prefix"],
        default="note",
        help="where to keep the folder name in the Proton export: in the entry note "
        "or as a prefix of the entry name (default: note)",
    )
    return parser.parse_args()
