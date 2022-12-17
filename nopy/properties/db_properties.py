from __future__ import annotations

from dataclasses import KW_ONLY
from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Type

from ..enums import NumberFormat
from ..enums import PropTypes
from ..exceptions import UnsupportedError
from .base import BaseProperty
from .common_properties import Option
from .common_properties import StatusGroup


@dataclass(eq=False)
class DBProp(BaseProperty):
    """The base class for all database properties.

    Attributes:
        name (str): The name of the property.
        id (str): The id of the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.UNSUPPORTED`.
    """

    name: str
    _: KW_ONLY
    id: str = ""

    def __post_init__(self):

        self._type = PropTypes.UNSUPPORTED

    @property
    def type(self) -> PropTypes:

        return self._type

    @classmethod
    def from_dict(cls: Type[DBProp], args: dict[str, Any]) -> DBProp:

        return DBProp(name=args["name"], id=args["id"])

    def serialize(self) -> dict[str, Any]:

        # This single implementation is enough for all the properties
        # that require no configuration data regarding the property.
        if self._type == PropTypes.UNSUPPORTED:
            raise UnsupportedError(
                "this is an unsupported or invalid database property"
            )
        return {self._type.value: {}, "name": self.name}


@dataclass(eq=False)
class DBCheckbox(DBProp):
    """A representation of a 'Checkbox' property in a database.

    Attributes:
        name (str): The name of the property.
        id (str): The id of the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.CHECKBOX`.
    """

    def __post_init__(self):
        self._type = PropTypes.CHECKBOX

    @classmethod
    def from_dict(cls: Type[DBCheckbox], args: dict[str, Any]) -> DBCheckbox:

        return DBCheckbox(name=args["name"], id=args["id"])

    def __hash__(self) -> int:
        return super().__hash__()


@dataclass(eq=False)
class DBCreatedBy(DBProp):
    """A representation of a 'Created By' property in a database.

    Attributes:
        name (str): The name of the property.
        id (str): The id of the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.CREATED_BY`.
    """

    def __post_init__(self):
        self._type = PropTypes.CREATED_BY

    @classmethod
    def from_dict(cls: Type[DBCreatedBy], args: dict[str, Any]) -> DBCreatedBy:

        return DBCreatedBy(name=args["name"], id=args["id"])

    def serialize(self) -> dict[str, Any]:
        raise UnsupportedError("'created_by' is not supported by the Notion API")


@dataclass(eq=False)
class DBCreatedTime(DBProp):
    """A representation of a 'Created Time' property in a database.

    Attributes:
        name (str): The name of the property.
        id (str): The id of the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.CREATED_TIME`.
    """

    def __post_init__(self):
        self._type = PropTypes.CREATED_TIME

    @classmethod
    def from_dict(cls: Type[DBCreatedTime], args: dict[str, Any]) -> DBCreatedTime:

        return DBCreatedTime(name=args["name"], id=args["id"])

    def serialize(self) -> dict[str, Any]:
        raise UnsupportedError("'created_time' is not supported by the Notion API")


@dataclass(eq=False)
class DBDate(DBProp):
    """A representation of a 'Date' property in a database.

    Attributes:
        name (str): The name of the property.
        id (str): The id of the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.DATE`.
    """

    def __post_init__(self):
        self._type = PropTypes.DATE

    @classmethod
    def from_dict(cls: Type[DBDate], args: dict[str, Any]) -> DBDate:

        return DBDate(name=args["name"], id=args["id"])


@dataclass(eq=False)
class DBEmail(DBProp):
    """A representation of a 'Email' property in a database.

    Attributes:
        name (str): The name of the property.
        id (str): The id of the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.EMAIL`.
    """

    def __post_init__(self):
        self._type = PropTypes.EMAIL

    @classmethod
    def from_dict(cls: Type[DBEmail], args: dict[str, Any]) -> DBEmail:

        return DBEmail(name=args["name"], id=args["id"])


@dataclass(eq=False)
class DBFiles(DBProp):
    """A representation of a 'Files' property in a database.

    Attributes:
        name (str): The name of the property.
        id (str): The id of the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.FILES`.
    """

    def __post_init__(self):
        self._type = PropTypes.FILES

    @classmethod
    def from_dict(cls: Type[DBFiles], args: dict[str, Any]) -> DBFiles:

        return DBFiles(name=args["name"], id=args["id"])


@dataclass(eq=False)
class DBFormula(DBProp):
    """A representation of a 'Formula' property in a database.

    Attributes:
        name (str): The name of the property.
        id (str): The id of the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.FORMULA`.
        expression (str): The formula to apply as a string.
    """

    expression: str = ""

    def __post_init__(self):

        self._type = PropTypes.FORMULA

    @classmethod
    def from_dict(cls: Type[DBFormula], args: dict[str, Any]) -> DBFormula:

        return DBFormula(
            name=args["name"], id=args["id"], expression=args["formula"]["expression"]
        )

    def serialize(self) -> dict[str, Any]:
        return {self._type.value: {"expression": self.expression}, "name": self.name}


@dataclass(eq=False)
class DBLastEditedBy(DBProp):
    """A representation of a 'Last Edited By' property in a database.

    Attributes:
        name (str): The name of the property.
        id (str): The id of the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.LAST_EDITED_BY`.
    """

    def __post_init__(self):
        self._type = PropTypes.LAST_EDITED_BY

    @classmethod
    def from_dict(cls: Type[DBLastEditedBy], args: dict[str, Any]) -> DBLastEditedBy:

        return DBLastEditedBy(name=args["name"], id=args["id"])

    def serialize(self) -> dict[str, Any]:
        raise UnsupportedError("'last_edited_by' is not supported by the Notion API")


@dataclass(eq=False)
class DBLastEditedTime(DBProp):
    """A representation of a 'Last Edited Time' property in a database.

    Attributes:
        name (str): The name of the property.
        id (str): The id of the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.LAST_EDITED_TIME`.
    """

    def __post_init__(self):
        self._type = PropTypes.LAST_EDITED_TIME

    @classmethod
    def from_dict(
        cls: Type[DBLastEditedTime], args: dict[str, Any]
    ) -> DBLastEditedTime:

        return DBLastEditedTime(name=args["name"], id=args["id"])

    def serialize(self) -> dict[str, Any]:
        raise UnsupportedError("'last_edited_time' is not supported by the Notion API")


@dataclass(eq=False)
class DBMultiSelect(DBProp):
    """A representation of a 'Multi Select' property in a database.

    Attributes:
        name (str): The name of the property.
        id (str): The id of the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.MULTI_SELECT`.
        options (list[Option]): The available options.
    """

    options: list[Option] = field(default_factory=list)

    def __post_init__(self):

        self._type = PropTypes.MULTI_SELECT

    @classmethod
    def from_dict(cls: Type[DBMultiSelect], args: dict[str, Any]) -> DBMultiSelect:

        options = [Option.from_dict(opt) for opt in args["multi_select"]["options"]]
        new_args: dict[str, Any] = {
            "name": args["name"],
            "id": args["id"],
            "options": options,
        }
        return DBMultiSelect(**new_args)

    def serialize(self) -> dict[str, Any]:
        serialized_options = [opt.serialize() for opt in self.options]
        return {self._type.value: {"options": serialized_options}, "name": self.name}


@dataclass(eq=False)
class DBNumber(DBProp):
    """A representation of a 'Number' property in a database.

    Attributes:
        name (str): The name of the property.
        id (str): The id of the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.NUMBER`.
        format (NumberFormat): The format of the number.
    """

    format: NumberFormat = NumberFormat.NUMBER

    def __post_init__(self):

        self._type = PropTypes.NUMBER

    @classmethod
    def from_dict(cls: Type[DBNumber], args: dict[str, Any]) -> DBNumber:

        new_args: dict[str, Any] = {
            "id": args["id"],
            "name": args["name"],
            "format": NumberFormat[args["number"]["format"].upper()],
        }

        return DBNumber(**new_args)

    def serialize(self) -> dict[str, Any]:
        return {self._type.value: {"format": self.format.value}, "name": self.name}


@dataclass(eq=False)
class DBPhoneNumber(DBProp):
    """A representation of a 'Phone Number' property in a database.

    Attributes:
        name (str): The name of the property.
        id (str): The id of the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.PHONE_NUMBER`.
    """

    def __post_init__(self):
        self._type = PropTypes.PHONE_NUMBER

    @classmethod
    def from_dict(cls: Type[DBPhoneNumber], args: dict[str, Any]) -> DBPhoneNumber:

        return DBPhoneNumber(name=args["name"], id=args["id"])


@dataclass(eq=False)
class DBSelect(DBProp):
    """A representation of a 'Select' property in a database.

    Attributes:
        name (str): The name of the property.
        id (str): The id of the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.SELECT`.
        options (list[Option]): The available options.
    """

    options: list[Option] = field(default_factory=list)

    def __post_init__(self):

        self._type = PropTypes.SELECT

    @classmethod
    def from_dict(cls: Type[DBSelect], args: dict[str, Any]) -> DBSelect:

        options = [Option.from_dict(opt) for opt in args["select"]["options"]]
        new_args: dict[str, Any] = {
            "name": args["name"],
            "id": args["id"],
            "options": options,
        }

        return DBSelect(**new_args)

    def serialize(self) -> dict[str, Any]:
        serialized_options = [opt.serialize() for opt in self.options]
        return {self._type.value: {"options": serialized_options}, "name": self.name}


@dataclass(eq=False)
class DBStatus(DBProp):
    """A representation of a 'Status' property in a database.

    Attributes:
        name (str): The name of the property.
        id (str): The id of the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.STATUS`.
        options (list[Option]): The available options.
        groups (list[Option]): The available groups.

    """

    options: list[Option] = field(default_factory=list)
    groups: list[StatusGroup] = field(default_factory=list)

    def __post_init__(self):

        self._type = PropTypes.STATUS

    @classmethod
    def from_dict(cls: Type[DBStatus], args: dict[str, Any]) -> DBStatus:

        options = [Option.from_dict(opt) for opt in args["status"]["options"]]
        groups = [StatusGroup.from_dict(grp) for grp in args["status"]["groups"]]
        new_args: dict[str, Any] = {
            "name": args["name"],
            "id": args["id"],
            "options": options,
            "groups": groups,
        }

        return DBStatus(**new_args)

    def serialize(self) -> dict[str, Any]:
        # Confirmed with Notion that they don't support it yet.
        raise UnsupportedError(
            "creating/updating 'status' types are not supported by the Notion API"
        )


@dataclass(eq=False)
class DBText(DBProp):
    """A representation of a 'Text' property in a database.

    Attributes:
        name (str): The name of the property.
        id (str): The id of the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.RICH_TEXT`.
    """

    def __post_init__(self):
        self._type = PropTypes.RICH_TEXT

    @classmethod
    def from_dict(cls: Type[DBText], args: dict[str, Any]) -> DBText:

        return DBText(name=args["name"], id=args["id"])


@dataclass(eq=False)
class DBTitle(DBProp):
    """A representation of a 'Title' property in a database.

    Attributes:
        name (str): The name of the property.
        id (str): The id of the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.TITLE`.
    """

    def __post_init__(self):
        self._type = PropTypes.TITLE

    @classmethod
    def from_dict(cls: Type[DBTitle], args: dict[str, Any]) -> DBTitle:

        return DBTitle(name=args["name"], id=args["id"])


@dataclass(eq=False)
class DBUrl(DBProp):
    """A representation of a 'Url' property in a database.

    Attributes:
        name (str): The name of the property.
        id (str): The id of the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.URL`.
    """

    def __post_init__(self):
        self._type = PropTypes.URL

    @classmethod
    def from_dict(cls: Type[DBUrl], args: dict[str, Any]) -> DBUrl:

        return DBUrl(name=args["name"], id=args["id"])
