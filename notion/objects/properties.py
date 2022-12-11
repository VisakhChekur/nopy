from typing import MutableMapping

from notion.typings import Props


class Properties(MutableMapping[str, Props]):
    def __init__(self):

        self._names: dict[str, Props] = {}
        self._ids: dict[str, Props] = {}

    def get(self, key: str):

        return self.__getitem__(key)

    def pop(self, key: str) -> Props:

        try:
            prop = self._names.pop(key)
            self._ids.pop(prop.id, None)
            return prop
        except KeyError:
            prop = self._ids.pop(key)
            self._names.pop(prop.name, None)
            return prop

    def add_prop(self, prop: Props):

        if prop.id:
            self._ids[prop.id] = prop
        if prop.name:
            self._names[prop.name] = prop

    def update_prop(self, key: str, prop: Props):
        """Updates the property based on the given key.

        This will delete the existing property with the given key
        and create a new key-value pair based on the new properties
        name and id. Use this ONLY if you want to change the property type
        of an already existing property. To edit an already existing property's
        details WITHOUT changing the property type, simply edit the property
        attributes after using the 'get' method.
        """
        old_prop = self.pop(key)
        # Need to set this right now since the 'prop.id' is used later during
        # serialization
        prop.id = old_prop.id
        self.add_prop(prop)

    def id_exists(self, key: str) -> bool:

        return key in self._ids

    def name_exists(self, key: str) -> bool:

        return key in self._names

    def get_ids(self):

        return self._ids.keys()

    def get_names(self):

        return self._names.keys()

    def iter_names(self):

        return self._names.items()

    def iter_ids(self):

        return self._ids.items()

    # ----- MUST Methods -----
    def __getitem__(self, key: str) -> Props:

        try:
            return self._names[key]
        except KeyError:
            return self._ids[key]

    def __setitem__(self, key: str, value: Props) -> None:
        raise NotImplementedError("use the 'set()' method instead")

    def __len__(self):
        return len(self._names)

    def __delitem__(self, key: str):

        try:
            prop = self._names.pop(key)
            self._ids.pop(prop.id, None)
        except KeyError:
            prop = self._ids.pop(key)
            self._names.pop(prop.name, None)

    def __iter__(self):

        return self._names.__iter__()

    def __str__(self):

        if self._names:
            return str(self._names)
        return str(self._ids)

    def __repr__(self):
        return repr(self._names)

    def __contains__(self, key: str) -> bool:  # type: ignore
        return key in self._ids or key in self._names
