from collections.abc import Collection
from typing import Set

from nopy.exceptions import PropertyExistsError
from nopy.exceptions import PropertyNotFoundError
from nopy.typings import Props


class Properties(Collection[Props]):
    def __init__(self):

        self._names: dict[str, Props] = {}
        self._ids: dict[str, Props] = {}
        self._props: Set[Props] = set()

    def get(self, prop: str) -> Props:

        return self.__getitem__(prop)

    def add(self, prop: Props):

        if prop in self:
            raise PropertyExistsError("property with same id or name already exists")

        self._props.add(prop)
        if prop.id:
            self._ids[prop.id] = prop
        if prop.name:
            self._names[prop.name] = prop

    def pop(self, prop: str) -> Props:

        try:
            popped = self._names.pop(prop, None)
            if not popped:
                return self._ids.pop(prop)
            return popped
        except KeyError:
            raise PropertyNotFoundError(
                f"property with name or id, {prop}, was not found"
            )

    def _pop_with_str(self, prop_identifier: str) -> Props:

        try:
            popped = self._names.pop(prop_identifier)
            self._ids.pop(popped.id)
        except KeyError:
            popped = self._ids.pop(prop_identifier)
            self._names.pop(popped.name)

        self._props.remove(popped)
        return popped

    # ----- Dunder Methods -----

    def __contains__(self, prop: object) -> bool:

        if isinstance(prop, Props):
            return prop.name in self._names or prop.id in self._ids

        return prop in self._names or prop in self._ids

    def __len__(self) -> int:
        return len(self._props)

    def __iter__(self):

        return self._props.__iter__()

    def __getitem__(self, key: str) -> Props:

        try:
            prop = self._names.get(key, None)
            if prop:
                return prop
            return self._ids[key]
        except KeyError:
            raise PropertyNotFoundError(
                "property with name or id, `{key}`, was not found"
            )
