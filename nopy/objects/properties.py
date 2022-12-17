from __future__ import annotations

from collections.abc import Collection
from typing import Any
from typing import Optional
from typing import Set

from nopy.exceptions import PropertyExistsError
from nopy.exceptions import PropertyNotFoundError
from nopy.exceptions import UnsupportedError
from nopy.typings import Props


class Properties(Collection[Props]):
    """A class that acts as a collection that holds all the properties of a
    Notion database or page."""

    def __init__(self):

        self._names: dict[str, Props] = {}
        self._ids: dict[str, Props] = {}
        self._props: Set[Props] = set()

    def get(self, prop_identifier: str) -> Props:
        """Returns the property with the given name or id.

        Raises:
            PropertyNotFoundError: Property with give name or id was not found.
        """

        return self.__getitem__(prop_identifier)

    def add(self, prop: Props):
        """Adds the given property.

        Raises:
            PropertyExistsError: Property with same id or name already exists.
        """

        if not prop.id and not prop.name:
            raise ValueError("'prop' must have a name or an id")

        if prop in self:
            raise PropertyExistsError("property with same id or name already exists")

        self._props.add(prop)
        if prop.id:
            self._ids[prop.id] = prop
        if prop.name:
            self._names[prop.name] = prop

    def pop(self, prop_identifier: str) -> Props:
        """Deletes and returns the property with the given name or id.

        Raises:
            PropertyNotFoundError: Property with give name or id was not found.
        """

        try:
            popped = self._names.pop(prop_identifier, None)
            if not popped:
                return self._ids.pop(prop_identifier)
            return popped
        except KeyError:
            raise PropertyNotFoundError(
                f"property with name or id, {prop_identifier}, was not found"
            )

    # ---- Private Methods ----

    def _pop_with_str(self, prop_identifier: str) -> Props:

        try:
            popped = self._names.pop(prop_identifier)
            self._ids.pop(popped.id)
        except KeyError:
            popped = self._ids.pop(prop_identifier)
            self._names.pop(popped.name)

        self._props.remove(popped)
        return popped

    @staticmethod
    def serialize(props: Properties, og_props: Optional[Set[str]] = None):

        serialized: dict[str, Any] = {}
        for prop in props._props:

            try:
                if prop.id:
                    serialized[prop.id] = prop.serialize()
                else:
                    serialized[prop.name] = prop.serialize()
            except UnsupportedError:
                continue

        # Handling deleted properties
        if og_props:
            # Finding the deleted properties
            curr_ids = set(props._ids.keys())
            deleted_prop_ids = og_props.difference(curr_ids)
            deleted_props = {prop_id: None for prop_id in deleted_prop_ids}
            serialized.update(deleted_props)

        return serialized

    # ----- Dunder Methods -----

    def __contains__(self, prop: object) -> bool:

        if isinstance(prop, Props):
            return prop.name in self._names or prop.id in self._ids

        return prop in self._names or prop in self._ids

    def __len__(self) -> int:
        return len(self._props)

    def __iter__(self):

        return self._props.__iter__()

    def __getitem__(self, prop_identifier: str) -> Props:

        try:
            prop = self._names.get(prop_identifier, None)
            if prop:
                return prop
            return self._ids[prop_identifier]
        except KeyError:
            raise PropertyNotFoundError(
                "property with name or id, `{key}`, was not found"
            )
