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
    return parser.parse_args()