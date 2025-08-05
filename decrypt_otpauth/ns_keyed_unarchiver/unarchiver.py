import plistlib
from typing import Any
from decrypt_otpauth.ns_keyed_unarchiver.types_ import NSType, Unarchiver
from decrypt_otpauth.ns_keyed_unarchiver.registry import NSTypeRegistry


class NSKeyedUnarchiver(Unarchiver):
    _registry = NSTypeRegistry()

    def __init__(self, data: bytes):
        self._plist = self._load_plist(data)
        self._objects = self._plist.get("$objects", {})

        self._cache = {}

    @property
    def info(self) -> dict:
        return {
            "version": self._plist.get("$version"),
            "archiver": self._plist.get("$archiver"),
            "object_count": len(self._objects),
            "top_keys": list(self._plist.get("$top", {}).keys())
        }

    def unarchive(self):
        top = self._plist.get("$top", {})
        root_ref = top.get("root")

        if not isinstance(root_ref, plistlib.UID):
            return None
        return self._unarchive_object(root_ref.data)

    def _unarchive_object(self, index: int):
        if index == 0:
            return None

        if index in self._cache:
            return self._cache[index]

        raw_obj = self._objects[index]
        if not isinstance(raw_obj, dict):  # primitive types
            return raw_obj

        class_ref = raw_obj.get('$class')
        if class_ref is None:
            return raw_obj

        class_info = self._objects[class_ref.data]
        class_name = class_info.get('$classname')
        result = self._registry.unarchive(class_name, raw_obj, self)

        self._cache[index] = result

        return result

    def _unarchive_by_class(self, class_name: str, obj: dict):
        pass

    def register_type(self, ns_type: type[NSType]) -> None:
        """
        Register a custom NSType handler.

        Args:
            ns_type: NSType subclass to register
        """
        self._registry.register(ns_type)

    def _resolve_ref(self, obj: Any) -> Any:
        if isinstance(obj, plistlib.UID):
            return self._unarchive_object(obj.data)
        return obj

    def _resolve_refs_in_dict(self, d: dict) -> dict:
        result = {}
        for key, value in d.items():
            if key.startswith('$'):  # skip metadata keys
                continue
            result[key] = self._resolve_ref(value)
        return result

    def _load_plist(self, data: bytes) -> dict:
        plist = plistlib.loads(data)
        self._check_is_ns_key_archiver(plist)
        return plist

    @staticmethod
    def _check_is_ns_key_archiver(plist) -> None:
        if plist.get("$archiver") == "NSKeyedArchiver":
            return
        msg = "no a valid NSKeyedArchiver plist provided"
        raise ValueError(msg)