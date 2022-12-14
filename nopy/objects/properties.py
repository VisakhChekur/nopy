from typing import MutableMapping

from nopy.typings import Props


class Properties(MutableMapping[str, Props]):
    """A dictionary-like object which can be used to access and set
    properties of any Notion object.

    NOTE: While it's possible to access properties as in a database using
    the square brackets (`properties["prop_name"]`), it's not possible to
    set properties using the square brackets.
    """

    def __init__(self):

        self._names: dict[str, Props] = {}
        self._ids: dict[str, Props] = {}

    def get(self, key: str) -> Props:
        """Get the property instance based on the given key.

        The key can be the `id` of the property, if it has one, or the `name`
        of the property, if it has one.

        Returns:
            The property.

        Raises:
            KeyError: No property exists with the given key (i.e. `id` or
            `name`).
        """
        return self.__getitem__(key)

    def pop(self, key: str) -> Props:
        """Delete the property based on the given key.

        The key can be the `id` of the property, if it has one, or the `name`
        of the property, if it has one.

        Returns:
            The property.

        Raises:
            KeyError: No property exists with the given key (i.e. `id` or
            `name`).
        """

        try:
            prop = self._names.pop(key)
            self._ids.pop(prop.id, None)
            return prop
        except KeyError:
            prop = self._ids.pop(key)
            self._names.pop(prop.name, None)
            return prop

    def add_prop(self, prop: Props):
        """Add a property."""

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
        """Returns a boolean indicating whether a property with the given
        `id` exists."""

        return key in self._ids

    def name_exists(self, key: str) -> bool:
        """Returns a boolean indicating whether a property with the given
        `name` exists."""

        return key in self._names

    def get_ids(self):
        """Returns the all the `ids` of the properties within this instance.

        NOTE: If there are properties that have no `id`, such as newly created
        properties, then those will be skipped.
        """

        return self._ids.keys()

    def get_names(self):
        """Returns the all the `names` of the properties within this instance.

        NOTE: If there are properties that have no `name` then those will be
        skipped.
        """

        return self._names.keys()

    def iter_names(self):
        """Iterate through the properties where the key is the `name` of
        the property."""

        return self._names.items()

    def iter_ids(self):
        """Iterate through the properties where the key is the `id` of
        the property."""

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
        # TODO: Implement this properly.
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
