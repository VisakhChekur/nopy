from collections.abc import Collection
from typing import Any
from typing import Iterable
from typing import Iterator
from typing import Optional
from typing import Set
from typing import Union

from nopy.errors import PropertyExistsError
from nopy.errors import PropertyNotFoundError
from nopy.errors import UnuspportedError
from nopy.types import Props


class Properties(Collection[Props]):
    """Holds the properties of a database/page."""

    def __init__(self, props: Optional[Iterable[Props]] = None):

        # The property names mapped to the corresponding property.
        self._names: dict[str, Props] = {}
        # The property ids mapped to the corresponding property.
        self._ids: dict[str, Props] = {}
        # Keeping this set makes handling __len__ and __iter__ easier.
        self._props: Set[Props] = set()

        if props is not None:
            for prop in props:
                self.add(prop)

    def add(self, prop: Props):
        """Adds the given property.

        Attributes:
            prop: The property to add.

        Raises:
            ValueError:
                Raised if property has neither name nor id.
            PropertyExistsError:
                Raised if a property that already exists is tried to be added
                again.
        """

        if not prop.name and not prop.id:
            raise ValueError("either id or name must be provided")
        if prop.name in self._names or prop.id in self._ids or prop in self._props:
            raise PropertyExistsError("'prop' already exists")

        if prop.name:
            self._names[prop.name] = prop
        if prop.id:
            self._ids[prop.id] = prop
        self._props.add(prop)

    def get(self, prop_identifier: str) -> Props:
        """Gets the property based on the given identifier.

        Attributes:
            prop_identifier: The name or the id of the property.

        Raises:
            KeyError: Raised if the property isn't found.
        """

        return self.__getitem__(prop_identifier)

    def pop(self, prop: Union[str, Props]) -> Props:
        """Deletes the property.

        Attributes:
            prop: The property to be deleted or it's id or name.

        Raises:
            KeyError: Raised if the property isn't found.
        """

        try:
            if isinstance(prop, str):
                prop = self.__getitem__(prop)

            self._props.remove(prop)
            self._names.pop(prop.name, None)
            self._ids.pop(prop.id, None)
            return prop
        except (KeyError, PropertyNotFoundError):
            msg = f"'{prop}' not found"
            raise PropertyNotFoundError(msg)

    def serialize(self) -> dict[str, Optional[dict[str, Any]]]:

        serialized: dict[str, Optional[dict[str, Any]]] = {}

        for prop in self._props:
            if prop.id:
                try:
                    serialized[prop.id] = prop.serialize()
                except UnuspportedError:
                    continue
            else:
                serialized[prop.name] = prop.serialize()

        return serialized

    # ----- Dunder Methods -----

    def __getitem__(self, prop_identifier: str):

        if prop := self._names.get(prop_identifier, None):
            return prop
        if prop := self._ids.get(prop_identifier, None):
            return prop

        msg = f"property with name or id '{prop_identifier}' not found"
        raise PropertyNotFoundError(msg)

    def __contains__(self, __x: object) -> bool:

        return __x in self._names or __x in self._ids or __x in self._props

    def __len__(self) -> int:

        return len(self._props)

    def __iter__(self) -> Iterator[Props]:

        return iter(self._props)

    def __str__(self) -> str:

        return str(self._props)
