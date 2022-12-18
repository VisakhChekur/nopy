from __future__ import annotations

from typing import Any
from typing import Type

from nopy.enums import PropTypes
from nopy.errors import UnsupportedByLibraryError


class BaseProperty:
    """The base class from which all properties inherit."""

    def serialize(self) -> dict[str, Any]:

        msg = f"serialization of '{self.__class__.__name__}' type properties"
        raise UnsupportedByLibraryError(msg)

    @classmethod
    def from_dict(cls: Type[BaseProperty], args: dict[str, Any]) -> BaseProperty:
        """Creates an instance of the object from the given dictionary.

        The dictionary MUST follow the format given by Notion.
        """
        raise NotImplementedError("to be implemented by subclass")


class ObjectProperty(BaseProperty):
    """The base class from which all properties directly available
    on databases and pages inherit."""

    def __init__(self):

        self._type: PropTypes = PropTypes.UNSUPPORTED

    @property
    def type(self) -> PropTypes:
        return self._type
