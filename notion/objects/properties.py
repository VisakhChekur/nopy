from typing import MutableMapping

from notion.typings import DBProps


class Properties(MutableMapping[str, DBProps]):
    def __init__(self):

        self._names: dict[str, DBProps] = {}
        self._ids: dict[str, DBProps] = {}

    def get(self, key: str):

        return self.__getitem__(key)

    def set(self, key: str, prop: DBProps, id: bool = False):

        if id:
            # Need to pop from the dictionary to handle cases where
            # the user is replacing the property for the given key
            self._ids.pop(key, None)
            self._ids[key] = prop
            self._names[prop.name] = prop
        else:
            self._names.pop(key, None)
            self._names[key] = prop
            self._ids[key] = prop

    def id_exists(self, key: str) -> bool:

        return key in self._ids

    def name_exists(self, key: str) -> bool:

        return key in self._names

    def _set_trusted(self, key: str, prop: DBProps):
        """Used when setting the properties after getting the values from a
        trusted source i.e. the Notion API. No need for extra checks provided
        in `set()`. The `key` is assumed to be the `id` of the property."""

        self._ids[key] = prop
        self._names[prop.name] = prop

    # ----- MUST Methods -----
    def __getitem__(self, key: str) -> DBProps:

        try:
            return self._names[key]
        except KeyError:
            return self._ids[key]

    def __setitem__(self, key: str, value: DBProps) -> None:
        raise NotImplementedError("use the 'set()' method instead")

    def __iter__(self):

        return self._names.__iter__()

    def __len__(self):
        return len(self._names)

    def __delitem__(self, key: str):

        try:
            self._names.pop(key)
        except KeyError:
            self._ids.pop(key)

    def __str__(self):
        return str(self._names)

    def __repr__(self):
        return repr(self._names)

    def __contains__(self, key: str) -> bool:  # type: ignore
        return key in self._ids or key in self._names
