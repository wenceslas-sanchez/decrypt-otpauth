import pathlib
import tempfile
from unittest import mock
from typing import Annotated
from urllib.parse import urlparse, parse_qs

import pytest
import cv2

from decrypt_otpauth.main import OTPAuthProcessor, main


@pytest.fixture
def test_file_path() -> pathlib.Path:
    return pathlib.Path(__file__).parent / "data" / "Accounts.otpauthdb"


@pytest.fixture
def test_password() -> str:
    return "hello"


def test_otpauth_processor_process_file(
    test_file_path: Annotated[pathlib.Path, pytest.fixture],
    test_password: Annotated[str, pytest.fixture],
):
    processor = OTPAuthProcessor()
    with mock.patch("getpass.getpass", return_value=test_password):
        folders = processor.process_file(str(test_file_path))

    assert isinstance(folders, dict)
    assert len(folders) > 0


def test_display_all_accounts_terminal_mode(
    test_file_path: Annotated[pathlib.Path, pytest.fixture],
    test_password: Annotated[str, pytest.fixture],
    capsys,
):
    processor = OTPAuthProcessor()
    with mock.patch("getpass.getpass", return_value=test_password):
        folders = processor.process_file(str(test_file_path))
    with mock.patch("builtins.input", return_value=""):
        processor.display_all_accounts(folders, images_location=None)

    captured = capsys.readouterr()
    assert "Folder" in captured.out or "Account" in captured.out


def test_main_terminal_mode(
    test_file_path: Annotated[pathlib.Path, pytest.fixture],
    test_password: Annotated[str, pytest.fixture],
):
    with mock.patch("sys.argv", ["main.py", "-p", str(test_file_path)]):
        with mock.patch("getpass.getpass", return_value=test_password):
            with mock.patch("builtins.input", return_value=""):
                result = main()
    assert result == 0


def test_main_with_wrong_password(
    test_file_path: Annotated[pathlib.Path, pytest.fixture],
):
    with mock.patch("sys.argv", ["main.py", "-p", str(test_file_path)]):
        with mock.patch("getpass.getpass", return_value="wrong_password"):
            result = main()
    assert result == 1


def test_qr_codes_are_valid_and_decodable(
    test_file_path: Annotated[pathlib.Path, pytest.fixture],
    test_password: Annotated[str, pytest.fixture],
):
    processor = OTPAuthProcessor()
    with mock.patch("getpass.getpass", return_value=test_password):
        folders = processor.process_file(str(test_file_path))

    with tempfile.TemporaryDirectory() as tmpdir:
        processor.display_all_accounts(folders, images_location=tmpdir)

        qr_images = list(pathlib.Path(tmpdir).glob("*.png"))
        assert len(qr_images) > 0, "No QR code images were generated"

        qr_decoder = cv2.QRCodeDetector()
        for qr_image_path in qr_images:
            image = cv2.imread(str(qr_image_path))
            decoded_data, points, _ = qr_decoder.detectAndDecode(image)

            parsed_uri = urlparse(decoded_data)
            assert parsed_uri.scheme == "otpauth"
            assert parsed_uri.netloc == "totp"

            params = parse_qs(parsed_uri.query)
            assert params["secret"][0] in ["HELLO", "OKOA"]
            assert params["issuer"][0] == "TestService"
            assert params["period"][0] == "30"
