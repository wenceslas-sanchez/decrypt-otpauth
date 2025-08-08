import urllib.parse
import urllib.request
from PIL import Image
import io

QR_URL_API = "https://api.qrserver.com/v1/create-qr-code/"


def fetch_and_display(uri: str) -> None:
    qr_code = _fetch_qrcode(uri)
    _display_qr_terminal(qr_code)


def _display_qr_terminal(image_data):
    buffer = io.BytesIO(image_data)
    img = Image.open(buffer).convert("L").resize((40, 40))

    for y in range(img.height):
        for x in range(img.width):
            pixel = img.getpixel((x, y))
            print("██" if pixel < 128 else "  ", end="")
        print()


def _fetch_qrcode(uri) -> bytes:
    qr_url = _create_qr_url_via_api(uri)
    with urllib.request.urlopen(qr_url) as response:
        image_data = response.read()
        # headers = response.info()
    return image_data


def _create_qr_url_via_api(uri: str):
    params = urllib.parse.urlencode(
        {
            "data": uri,
            "ecc": "L",  # Error correction level
            "size": "200x200",
        }
    )
    return f"{QR_URL_API}?{params}"
