from __future__ import annotations

from typing import Any
from typing import Type


class BaseProperty:
    """The base class from which all properties inherit."""

    @classmethod
    def from_dict(cls: Type[BaseProperty], args: dict[str, Any]) -> BaseProperty:
        """Creates an instance of this class from a dictionary that follows
        the Notion API spec."""
        raise NotImplementedError("to be implemented by subclass")

    def serialize(self) -> dict[str, Any]:
        raise NotImplementedError("to be implemented by subclass")


# TODO: Type hinting issues with abstractclass

# class BaseProperty(metaclass=ABCMeta):
#     """The base class from which all properties inherit."""

#     @abstractclassmethod
#     def from_dict(cls: Type[ABCMeta], args: dict[str, Any]) -> BaseProperty:
#         raise NotImplementedError()