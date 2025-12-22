import pathlib
import tempfile
from unittest import mock
from typing import Annotated

import pytest

from decrypt_otpauth.main import OTPAuthProcessor, main


@pytest.fixture
def test_file_path() -> pathlib.Path:
    return pathlib.Path(__file__).parent / "data" / "Accounts.otpauthdb"


@pytest.fixture
def test_password() -> str:
    return "hello"


@pytest.fixture
def expected_filename() -> list[str]:
    return ["test1_9b3ae5.png", "test2_016377.png"]


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


def test_display_all_accounts_image_mode(
    test_file_path: Annotated[pathlib.Path, pytest.fixture],
    test_password: Annotated[str, pytest.fixture],
    expected_filename: Annotated[list[str], pytest.fixture],
):
    processor = OTPAuthProcessor()
    with mock.patch("getpass.getpass", return_value=test_password):
        folders = processor.process_file(str(test_file_path))

    with tempfile.TemporaryDirectory() as tmpdir:
        processor.display_all_accounts(folders, images_location=tmpdir)
        image_files = [f.name for f in pathlib.Path(tmpdir).glob("*.png")]
    assert image_files == expected_filename


def test_main_with_images_location(
    test_file_path: Annotated[pathlib.Path, pytest.fixture],
    test_password: Annotated[str, pytest.fixture],
    expected_filename: Annotated[list[str], pytest.fixture],
):
    with tempfile.TemporaryDirectory() as tmpdir:
        with mock.patch(
            "sys.argv",
            ["main.py", "-p", str(test_file_path), "--images-location", tmpdir],
        ):
            with mock.patch("getpass.getpass", return_value=test_password):
                result = main()
        assert result == 0
        image_files = [f.name for f in pathlib.Path(tmpdir).glob("*.png")]
    assert image_files == expected_filename


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
