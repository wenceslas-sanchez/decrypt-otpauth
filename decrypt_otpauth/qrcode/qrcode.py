import qrcode


def fetch_and_display(uri: str) -> None:
    """Display QR code for the given URI in terminal"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=1,
        border=1,
    )
    qr.add_data(uri)
    qr.make(fit=True)
    qr.print_ascii()
