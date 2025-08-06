from abc import ABC, abstractmethod
from typing import Any, Protocol


class Unarchiver(Protocol):
    """Protocol defining the interface that NSType handlers need"""

    def _resolve_ref(self, obj: Any) -> Any:
        """Resolve a UID reference to its actual object"""

    def _resolve_refs_in_dict(self, d: dict) -> dict:
        """Recursively resolve UID references in a dictionary"""


class NSType(ABC):
    """Abstract base class for NSKeyedArchiver types"""

    @classmethod
    @abstractmethod
    def class_names(cls) -> list[str]:
        """Return list of Objective-C class names this type handles"""

    @classmethod
    @abstractmethod
    def unarchive(cls, obj: dict, unarchiver: Unarchiver) -> Any:
        """
        Unarchive an object of this type.

        Args:
            obj: The raw object dictionary
            unarchiver: Reference to the unarchiver for resolving references

        Returns:
            The unarchived Python object
        """


class NSString(NSType):
    """Handler for NSString and NSMutableString"""

    @classmethod
    def class_names(cls) -> list[str]:
        return ["NSString", "NSMutableString"]

    @classmethod
    def unarchive(cls, obj: dict, unarchiver: Unarchiver) -> str:
        return obj.get("NS.string", "")


class NSNumber(NSType):
    """Handler for NSNumber"""

    @classmethod
    def class_names(cls) -> list[str]:
        return ["NSNumber"]

    @classmethod
    def unarchive(cls, obj: dict, unarchiver: Unarchiver) -> int | float | bool:
        if "NS.intval" in obj:
            return obj["NS.intval"]
        elif "NS.dblval" in obj:
            return obj["NS.dblval"]
        elif "NS.boolval" in obj:
            return bool(obj["NS.boolval"])
        return 0


class NSData(NSType):
    """Handler for NSData and NSMutableData"""

    @classmethod
    def class_names(cls) -> list[str]:
        return ["NSData", "NSMutableData"]

    @classmethod
    def unarchive(cls, obj: dict, unarchiver: Unarchiver) -> bytes:
        return obj.get("NS.data", b"")


class NSDate(NSType):
    """Handler for NSDate"""

    @classmethod
    def class_names(cls) -> list[str]:
        return ["NSDate"]

    @classmethod
    def unarchive(cls, obj: dict, unarchiver: Unarchiver) -> float:
        # NSDate uses seconds since 2001-01-01 00:00:00 UTC
        timestamp = obj.get("NS.time", 0)
        # Convert to Unix timestamp: add seconds between 1970 and 2001
        return timestamp + 978307200


class NSArray(NSType):
    """Handler for NSArray and NSMutableArray"""

    @classmethod
    def class_names(cls) -> list[str]:
        return ["NSArray", "NSMutableArray"]

    @classmethod
    def unarchive(cls, obj: dict, unarchiver: Unarchiver) -> list[Any]:
        object_refs = obj.get("NS.objects", [])
        return [unarchiver._resolve_ref(ref) for ref in object_refs]


class NSDictionary(NSType):
    """Handler for NSDictionary and NSMutableDictionary"""

    @classmethod
    def class_names(cls) -> list[str]:
        return ["NSDictionary", "NSMutableDictionary"]

    @classmethod
    def unarchive(cls, obj: dict, unarchiver: Unarchiver) -> dict:
        if "NS.keys" in obj and "NS.objects" in obj:
            keys = obj.get("NS.keys", [])
            values = obj.get("NS.objects", [])
            result = {}
            for key_uid, value_uid in zip(keys, values):
                key = unarchiver._resolve_ref(key_uid)
                value = unarchiver._resolve_ref(value_uid)
                result[key] = value
            return result
        return unarchiver._resolve_refs_in_dict(obj)
