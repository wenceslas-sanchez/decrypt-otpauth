import json
import pathlib
import tempfile
import uuid
from typing import Annotated
from unittest import mock

import pytest

from decrypt_otpauth.main import OTPAuthProcessor, main
from decrypt_otpauth.otpauth.types_ import Folder
from decrypt_otpauth.proton.export import FolderPlacement, ProtonExporter


@pytest.fixture
def test_file_path() -> pathlib.Path:
    return pathlib.Path(__file__).parent.parent / "data" / "Accounts.otpauthdb"


@pytest.fixture
def folders(
    test_file_path: Annotated[pathlib.Path, pytest.fixture],
) -> dict[str, Folder]:
    processor = OTPAuthProcessor()
    with mock.patch("getpass.getpass", return_value="hello"):
        return processor.process_file(str(test_file_path))


@pytest.fixture
def expected_uris() -> list[str]:
    path = pathlib.Path(__file__).parent.parent / "data" / "expected_uris.txt"
    return path.read_text(encoding="utf-8").splitlines()


def test_build_export_folder_in_note(
    folders: Annotated[dict[str, Folder], pytest.fixture],
    expected_uris: Annotated[list[str], pytest.fixture],
):
    export = ProtonExporter().build_export(folders)

    assert export["version"] == 1
    assert [entry["content"]["uri"] for entry in export["entries"]] == expected_uris
    for entry in export["entries"]:
        uuid.UUID(entry["id"])
        assert entry["content"]["entry_type"] == "Totp"
        assert entry["content"]["name"] in ["test1", "test2"]
        assert entry["note"] == "Default Folder"


def test_build_export_folder_as_prefix(
    folders: Annotated[dict[str, Folder], pytest.fixture],
):
    export = ProtonExporter(folder_placement=FolderPlacement.PREFIX).build_export(
        folders
    )

    names = [entry["content"]["name"] for entry in export["entries"]]
    assert names == ["Default Folder - test1", "Default Folder - test2"]
    assert all(entry["note"] is None for entry in export["entries"])


def test_build_export_skips_hotp():
    account = {
        "secret": b"hello",
        "label": "counter",
        "period": 30,
        "type_": 1,
        "issuer": "TestService",
        "digits": 6,
        "algorithm": 1,
        "counter": 3,
    }
    export = ProtonExporter().build_export({"Work": Folder("Work", [account])})
    assert export["entries"] == []


def test_main_export_proton(test_file_path: Annotated[pathlib.Path, pytest.fixture]):
    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = pathlib.Path(tmpdir) / "proton.json"
        argv = [
            "main.py",
            "-p",
            str(test_file_path),
            "--export-proton",
            str(output_file),
        ]
        with mock.patch("sys.argv", argv):
            with mock.patch("getpass.getpass", return_value="hello"):
                assert main() == 0

        export = json.loads(output_file.read_text(encoding="utf-8"))
        assert len(export["entries"]) == 2
