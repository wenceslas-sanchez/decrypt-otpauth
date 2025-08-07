from typing import Any
from abc import abstractmethod


class ReverseEnumMixin:
    """Mixin class that provides default implementation for ReverseEnum protocol"""

    @property
    @abstractmethod
    def name_value(self) -> Any:
        """"""

    @classmethod
    def from_reverse_key(cls, key: str):
        for item in cls:
            if item.name_value == key:
                return item
        return next(iter(cls))
