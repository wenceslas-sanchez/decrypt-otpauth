import plistlib

import pytest
from typing import Callable, Annotated


@pytest.fixture
def plist_to_bytes() -> Callable[[dict], bytes]:
    def _plist_to_bytes(data: dict) -> bytes:
        return plistlib.dumps(data, fmt=plistlib.FMT_BINARY)

    return _plist_to_bytes


@pytest.fixture
def string_plist(
    plist_to_bytes: Annotated[Callable[[dict], bytes], pytest.fixture],
) -> bytes:
    return plist_to_bytes(
        {
            "$version": 100000,
            "$archiver": "NSKeyedArchiver",
            "$top": {"root": plistlib.UID(1)},
            "$objects": [
                "$null",
                {"NS.string": "Hello, World!", "$class": plistlib.UID(2)},
                {"$classes": ["NSString", "NSObject"], "$classname": "NSString"},
            ],
        }
    )


@pytest.fixture
def number_plist(
    plist_to_bytes: Annotated[Callable[[dict], bytes], pytest.fixture],
) -> bytes:
    return plist_to_bytes(
        {
            "$version": 100000,
            "$archiver": "NSKeyedArchiver",
            "$top": {"root": plistlib.UID(1)},
            "$objects": [
                "$null",
                {
                    "integer": plistlib.UID(2),
                    "float": plistlib.UID(3),
                    "boolean_true": plistlib.UID(4),
                    "boolean_false": plistlib.UID(5),
                    "$class": plistlib.UID(6),
                },
                {"NS.intval": 42, "$class": plistlib.UID(7)},
                {"NS.dblval": 3.14159, "$class": plistlib.UID(7)},
                {"NS.boolval": True, "$class": plistlib.UID(7)},
                {"NS.boolval": False, "$class": plistlib.UID(7)},
                {
                    "$classes": ["NSDictionary", "NSObject"],
                    "$classname": "NSDictionary",
                },
                {
                    "$classes": ["NSNumber", "NSValue", "NSObject"],
                    "$classname": "NSNumber",
                },
            ],
        }
    )


@pytest.fixture
def dictionary_plist(
    plist_to_bytes: Annotated[Callable[[dict], bytes], pytest.fixture],
) -> bytes:
    return plist_to_bytes(
        {
            "$version": 100000,
            "$archiver": "NSKeyedArchiver",
            "$top": {"root": plistlib.UID(1)},
            "$objects": [
                "$null",
                {
                    "NS.keys": [plistlib.UID(2), plistlib.UID(3), plistlib.UID(4)],
                    "NS.objects": [plistlib.UID(5), plistlib.UID(6), plistlib.UID(7)],
                    "$class": plistlib.UID(8),
                },
                {"NS.string": "name", "$class": plistlib.UID(9)},
                {"NS.string": "age", "$class": plistlib.UID(9)},
                {"NS.string": "active", "$class": plistlib.UID(9)},
                {"NS.string": "John Doe", "$class": plistlib.UID(9)},
                {"NS.intval": 30, "$class": plistlib.UID(10)},
                {"NS.boolval": True, "$class": plistlib.UID(10)},
                {
                    "$classes": ["NSDictionary", "NSObject"],
                    "$classname": "NSDictionary",
                },
                {"$classes": ["NSString", "NSObject"], "$classname": "NSString"},
                {
                    "$classes": ["NSNumber", "NSValue", "NSObject"],
                    "$classname": "NSNumber",
                },
            ],
        }
    )


@pytest.fixture
def array_plist(
    plist_to_bytes: Annotated[Callable[[dict], bytes], pytest.fixture],
) -> bytes:
    return plist_to_bytes(
        {
            "$version": 100000,
            "$archiver": "NSKeyedArchiver",
            "$top": {"root": plistlib.UID(1)},
            "$objects": [
                "$null",
                {
                    "NS.objects": [
                        plistlib.UID(2),
                        plistlib.UID(3),
                        plistlib.UID(4),
                        plistlib.UID(5),
                    ],
                    "$class": plistlib.UID(9),
                },
                {"NS.string": "Array Element 1", "$class": plistlib.UID(10)},
                {"NS.intval": 999, "$class": plistlib.UID(11)},
                {"NS.data": b"Hello Binary World!", "$class": plistlib.UID(12)},
                {
                    "NS.keys": [plistlib.UID(6)],
                    "NS.objects": [plistlib.UID(7)],
                    "$class": plistlib.UID(8),
                },
                {"NS.string": "nested_key", "$class": plistlib.UID(10)},
                {"NS.string": "nested_value", "$class": plistlib.UID(10)},
                {
                    "$classes": ["NSDictionary", "NSObject"],
                    "$classname": "NSDictionary",
                },
                {"$classes": ["NSArray", "NSObject"], "$classname": "NSArray"},
                {"$classes": ["NSString", "NSObject"], "$classname": "NSString"},
                {
                    "$classes": ["NSNumber", "NSValue", "NSObject"],
                    "$classname": "NSNumber",
                },
                {"$classes": ["NSData", "NSObject"], "$classname": "NSData"},
            ],
        }
    )


@pytest.fixture
def date_plist(
    plist_to_bytes: Annotated[Callable[[dict], bytes], pytest.fixture],
) -> bytes:
    return plist_to_bytes(
        {
            "$version": 100000,
            "$archiver": "NSKeyedArchiver",
            "$top": {"root": plistlib.UID(1)},
            "$objects": [
                "$null",
                {
                    "creation_date": plistlib.UID(2),
                    "timestamp_now": plistlib.UID(3),
                    "$class": plistlib.UID(4),
                },
                {"NS.time": 0.0, "$class": plistlib.UID(5)},  # 2001-01-01 00:00:00 UTC
                {"NS.time": 725846400.0, "$class": plistlib.UID(5)},  # ~2024-01-01
                {
                    "$classes": ["NSDictionary", "NSObject"],
                    "$classname": "NSDictionary",
                },
                {"$classes": ["NSDate", "NSObject"], "$classname": "NSDate"},
            ],
        }
    )


@pytest.fixture
def complexe_plist(
    plist_to_bytes: Annotated[Callable[[dict], bytes], pytest.fixture],
) -> bytes:
    return plist_to_bytes(
        {
            "$version": 100000,
            "$archiver": "NSKeyedArchiver",
            "$top": {"root": plistlib.UID(1)},
            "$objects": [
                "$null",
                {
                    "accounts": plistlib.UID(2),
                    "version": plistlib.UID(9),
                    "$class": plistlib.UID(10),
                },
                {
                    "NS.objects": [plistlib.UID(3), plistlib.UID(6)],
                    "$class": plistlib.UID(11),
                },
                {
                    "NS.keys": [plistlib.UID(4), plistlib.UID(5)],
                    "NS.objects": [plistlib.UID(12), plistlib.UID(13)],
                    "$class": plistlib.UID(10),
                },
                {"NS.string": "name", "$class": plistlib.UID(14)},
                {"NS.string": "secret", "$class": plistlib.UID(14)},
                {
                    "NS.keys": [plistlib.UID(4), plistlib.UID(5)],
                    "NS.objects": [plistlib.UID(7), plistlib.UID(8)],
                    "$class": plistlib.UID(10),
                },
                {"NS.string": "Google", "$class": plistlib.UID(14)},
                {"NS.data": b"JBSWY3DPEHPK3PXP", "$class": plistlib.UID(15)},
                {"NS.dblval": 1.1, "$class": plistlib.UID(16)},
                {
                    "$classes": ["NSDictionary", "NSObject"],
                    "$classname": "NSDictionary",
                },
                {"$classes": ["NSArray", "NSObject"], "$classname": "NSArray"},
                {"NS.string": "GitHub", "$class": plistlib.UID(14)},
                {
                    "NS.data": b"MFRGG2LTEB3GS5LQMFXHC5DSMR2W45A",
                    "$class": plistlib.UID(15),
                },
                {"$classes": ["NSString", "NSObject"], "$classname": "NSString"},
                {"$classes": ["NSData", "NSObject"], "$classname": "NSData"},
                {
                    "$classes": ["NSNumber", "NSValue", "NSObject"],
                    "$classname": "NSNumber",
                },
            ],
        }
    )
