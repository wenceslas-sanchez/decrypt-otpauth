import hashlib
import os
import pathlib

import qrcode


def fetch_and_display(uri: str) -> None:
    """Display QR code for the given URI in terminal"""
    qr = _make_qrcode(uri, box_size=1, border=1)
    qr.print_ascii()


def save_as_image(uri: str, images_location: str, account_label: str) -> None:
    """Save QR code as an image file

    Args:
        uri: The OTP URI to encode as QR code
        images_location: Directory path to save QR code image
        account_label: Account label to use in filename
    """
    qr = _make_qrcode(uri, box_size=10, border=4)
    image = qr.make_image(fill_color="black", back_color="white")
    filename = _get_filename(uri, account_label)
    _save_image(image, images_location, filename)


def _make_qrcode(uri: str, *args, **kwargs) -> qrcode.QRCode:
    qr = qrcode.QRCode(
        version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, *args, **kwargs
    )
    qr.add_data(uri)
    qr.make(fit=True)
    return qr


def _get_filename(uri: str, account_label: str) -> str:
    safe_label = "".join(
        c if c.isalnum() or c in (" ", "-", "_") else "_" for c in account_label
    )
    uri_hash = hashlib.sha256(uri.encode()).hexdigest()[:6]
    return f"{safe_label}_{uri_hash}.png"


def _save_image(image, images_location: str, filename: str) -> None:
    os.makedirs(images_location, exist_ok=True)
    filepath = pathlib.Path(images_location) / filename
    image.save(filepath)
