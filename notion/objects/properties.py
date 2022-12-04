
from notion.properties.db_props import DBProp

# TODO: Refactor this to use just one implementation?

# __delitem__, __getitem__, __iter__, __len__, __setitem__
class Properties(dict[str, DBProp]):
    """A dictionary thta holds the proerties of a database.
    
    Properties can be accessed using it's name or it's id. Accessing
    using 'id' is only possible if the 'id' is not empty (in the
    case of a newly created property by the user).
    """

    def __init__(self):

        self._ids: dict[str, DBProp] = {}
        self._name: dict[str, DBProp] = {}

    def set(self, key: str, value: DBProp, id:bool=False):
        """Adds the given property.
        
        Args:
            key:
                The name or the id of the property.
            value:
                The property instance.
            id:
                If `True`, then the key is considered as the property id.
        """

        # __setitem__ can't be implemented
        if not key:
            raise ValueError("'key' can't be an empty string")

        if id:
            self._ids[key] = value
            self._name[value.name] = value
        else:
            self._name[key] = value
            self._ids[value.id] = value

    def get(self, key: str) -> DBProp:
        """Returns the database property with the given name or id.
        
        Args:
            key:
                The name or id of the property. 

        Returns:
            The instance of the DBProp.
        
        Raises:
            KeyError: Invalid name or id.
        """

        return self.__getitem__(key)

    def pop(self, key: str):
        """Deletes the property with the given name or id.
        
        Raises:
            KeyError: Invalid name or id.
        """

        self.__delitem__(key)

    def __delitem__(self, key: str):
        
        try:
            prop = self._name.pop(key)
            if prop.id:
                self._ids.pop(prop.id)
        except KeyError:
            prop = self._ids.pop(key)
            self._name.pop(prop.name)

    def __getitem__(self, key: str) -> DBProp:
        
        val = self._name.get(key, None)
        if not val:
            val = self._ids.get(key, None)
        if val:
            return val
        raise KeyError(f"no property with '{key}' as 'id' or 'name' found")


    def __iter__(self):
        
        return self._name.__iter__()

    def __len__(self):
        
        return len(self._name)
