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
    return parser.parse_args()
