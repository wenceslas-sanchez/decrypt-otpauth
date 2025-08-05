from typing import Any

from decrypt_otpauth.ns_keyed_unarchiver.types_ import NSType, NSData, NSDate, NSArray, NSNumber, NSString, \
    NSDictionary, Unarchiver


class NSTypeRegistry:
    """Registry for NSType handlers"""

    def __init__(self):
        self._handlers: dict[str, type[NSType]] = {}

        self.register(NSString)
        self.register(NSNumber)
        self.register(NSData)
        self.register(NSDate)
        self.register(NSArray)
        self.register(NSDictionary)

    def register(self, ns_type: type[NSType]) -> None:
        """Register an NSType handler"""
        for class_name in ns_type.class_names():
            self._handlers[class_name] = ns_type

    def get_handler(self, class_name: str) -> type[NSType]:
        """Get handler for a class name"""
        return self._handlers.get(class_name)

    def unarchive(self, class_name: str, obj: dict, unarchiver: Unarchiver) -> Any:
        """Unarchive an object using the appropriate handler"""
        if (handler := self.get_handler(class_name)) is None:
            return unarchiver._resolve_refs_in_dict(obj)
        return handler.unarchive(obj, unarchiver)
