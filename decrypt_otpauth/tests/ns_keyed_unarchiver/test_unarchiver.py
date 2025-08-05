from decrypt_otpauth.ns_keyed_unarchiver.unarchiver import NSKeyedUnarchiver
from typing import Annotated
import pytest


def test_unarchive_string_plist(string_plist: Annotated[bytes, pytest.fixture]):
    assert NSKeyedUnarchiver(string_plist).unarchive() == "Hello, World!"


def test_unarchive_dictionary_list(dictionary_plist: Annotated[bytes, pytest.fixture]):
    assert NSKeyedUnarchiver(dictionary_plist).unarchive() == {
        "name": "John Doe",
        "age": 30,
        "active": True,
    }


def test_unarchive_numbers_plist(number_plist: Annotated[bytes, pytest.fixture]):
    assert NSKeyedUnarchiver(number_plist).unarchive() == {
        "boolean_false": False,
        "boolean_true": True,
        "float": 3.14159,
        "integer": 42,
    }


def test_unarchive_array_plist(array_plist: Annotated[bytes, pytest.fixture]):
    assert NSKeyedUnarchiver(array_plist).unarchive() == [
        "Array Element 1",
        999,
        b"Hello Binary World!",
        {"nested_key": "nested_value"},
    ]


def test_unarchive_date_plist(date_plist: Annotated[bytes, pytest.fixture]):
    assert NSKeyedUnarchiver(date_plist).unarchive() == {
        "creation_date": 978307200.0,
        "timestamp_now": 1704153600.0,
    }


def test_unarchive_complexe_plist(complexe_plist: Annotated[bytes, pytest.fixture]):
    assert NSKeyedUnarchiver(complexe_plist).unarchive() == {
        "accounts": [
            {"name": "GitHub", "secret": b"MFRGG2LTEB3GS5LQMFXHC5DSMR2W45A"},
            {"name": "Google", "secret": b"JBSWY3DPEHPK3PXP"},
        ],
        "version": 1.1,
    }
