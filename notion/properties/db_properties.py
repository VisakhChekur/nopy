from __future__ import annotations

from dataclasses import KW_ONLY
from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Iterable
from typing import Type

from notion.exceptions import UnsupportedError
from notion.properties.base import BaseProperty
from notion.properties.common_properties import Option
from notion.properties.common_properties import StatusGroup
from notion.properties.prop_enums import NumberFormat
from notion.properties.prop_enums import PropTypes

# Unsupported = people,


@dataclass
class DBProp(BaseProperty):

    name: str
    _: KW_ONLY
    id: str = ""

    def __post_init__(self):

        self.type = PropTypes.UNSUPPORTED

    @classmethod
    def from_dict(cls: Type[DBProp], args: dict[str, Any]) -> DBProp:

        return DBProp(name=args["name"], id=args["id"])

    def serialize(self) -> dict[str, Any]:

        # This single implementation is enough for all the properties
        # that require no configuration data regarding the property.
        if self.type == PropTypes.UNSUPPORTED:
            raise UnsupportedError(
                "this is an unsupported or invalid database property"
            )
        return {self.type.value: {}, "name": self.name}


@dataclass
class DBTitle(DBProp):
    def __post_init__(self):
        self.type = PropTypes.TITLE

    @classmethod
    def from_dict(cls: Type[DBTitle], args: dict[str, Any]) -> DBTitle:

        return DBTitle(name=args["name"], id=args["id"])


@dataclass
class DBText(DBProp):
    def __post_init__(self):
        self.type = PropTypes.RICH_TEXT

    @classmethod
    def from_dict(cls: Type[DBText], args: dict[str, Any]) -> DBText:

        return DBText(name=args["name"], id=args["id"])


@dataclass
class DBDate(DBProp):
    def __post_init__(self):
        self.type = PropTypes.DATE

    @classmethod
    def from_dict(cls: Type[DBDate], args: dict[str, Any]) -> DBDate:

        return DBDate(name=args["name"], id=args["id"])


@dataclass
class DBFiles(DBProp):
    def __post_init__(self):
        self.type = PropTypes.FILES

    @classmethod
    def from_dict(cls: Type[DBFiles], args: dict[str, Any]) -> DBFiles:

        return DBFiles(name=args["name"], id=args["id"])


@dataclass
class DBCheckbox(DBProp):
    def __post_init__(self):
        self.type = PropTypes.CHECKBOX

    @classmethod
    def from_dict(cls: Type[DBCheckbox], args: dict[str, Any]) -> DBCheckbox:

        return DBCheckbox(name=args["name"], id=args["id"])


@dataclass
class DBUrl(DBProp):
    def __post_init__(self):
        self.type = PropTypes.URL

    @classmethod
    def from_dict(cls: Type[DBUrl], args: dict[str, Any]) -> DBUrl:

        return DBUrl(name=args["name"], id=args["id"])


@dataclass
class DBEmail(DBProp):
    def __post_init__(self):
        self.type = PropTypes.EMAIL

    @classmethod
    def from_dict(cls: Type[DBEmail], args: dict[str, Any]) -> DBEmail:

        return DBEmail(name=args["name"], id=args["id"])


@dataclass
class DBPhoneNumber(DBProp):
    def __post_init__(self):
        self.type = PropTypes.PHONE_NUMBER

    @classmethod
    def from_dict(cls: Type[DBPhoneNumber], args: dict[str, Any]) -> DBPhoneNumber:

        return DBPhoneNumber(name=args["name"], id=args["id"])


@dataclass
class DBCreatedTime(DBProp):
    def __post_init__(self):
        self.type = PropTypes.CREATED_TIME

    @classmethod
    def from_dict(cls: Type[DBCreatedTime], args: dict[str, Any]) -> DBCreatedTime:

        return DBCreatedTime(name=args["name"], id=args["id"])

    def serialize(self) -> dict[str, Any]:
        raise UnsupportedError("'created_time' is not supported by the Notion API")


@dataclass
class DBCreatedBy(DBProp):
    def __post_init__(self):
        self.type = PropTypes.CREATED_BY

    @classmethod
    def from_dict(cls: Type[DBCreatedBy], args: dict[str, Any]) -> DBCreatedBy:

        return DBCreatedBy(name=args["name"], id=args["id"])

    def serialize(self) -> dict[str, Any]:
        raise UnsupportedError("'created_by' is not supported by the Notion API")


@dataclass
class DBLastEditedTime(DBProp):
    def __post_init__(self):
        self.type = PropTypes.LAST_EDITED_TIME

    @classmethod
    def from_dict(
        cls: Type[DBLastEditedTime], args: dict[str, Any]
    ) -> DBLastEditedTime:

        return DBLastEditedTime(name=args["name"], id=args["id"])

    def serialize(self) -> dict[str, Any]:
        raise UnsupportedError("'last_edited_time' is not supported by the Notion API")


@dataclass
class DBLastEditedBy(DBProp):
    def __post_init__(self):
        self.type = PropTypes.LAST_EDITED_BY

    @classmethod
    def from_dict(cls: Type[DBLastEditedBy], args: dict[str, Any]) -> DBLastEditedBy:

        return DBLastEditedBy(name=args["name"], id=args["id"])

    def serialize(self) -> dict[str, Any]:
        raise UnsupportedError("'last_edited_by' is not supported by the Notion API")


@dataclass
class DBNumber(DBProp):

    format: NumberFormat = NumberFormat.NUMBER

    def __post_init__(self):

        self.type = PropTypes.NUMBER

    @classmethod
    def from_dict(cls: Type[DBNumber], args: dict[str, Any]) -> DBNumber:

        new_args: dict[str, Any] = {
            "id": args["id"],
            "name": args["name"],
            "format": NumberFormat[args["number"]["format"].upper()],
        }

        return DBNumber(**new_args)

    def serialize(self) -> dict[str, Any]:
        return {self.type.value: {"format": self.format.value}, "name": self.name}


@dataclass
class DBSelect(DBProp):

    options: Iterable[Option] = field(default_factory=list)

    def __post_init__(self):

        self.type = PropTypes.SELECT

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
        return {self.type.value: {"options": serialized_options}, "name": self.name}


@dataclass
class DBMultiSelect(DBProp):

    options: Iterable[Option] = field(default_factory=list)

    def __post_init__(self):

        self.type = PropTypes.MULTI_SELECT

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
        return {self.type.value: {"options": serialized_options}, "name": self.name}


# TODO: How to create a status property on a DB being created?
@dataclass
class DBStatus(DBProp):

    options: Iterable[Option] = field(default_factory=list)
    groups: Iterable[StatusGroup] = field(default_factory=list)

    def __post_init__(self):

        self.type = PropTypes.STATUS

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
        # TODO: Confirm with Notion.
        raise UnsupportedError("'status' types are not supported by the Notion API")


@dataclass
class DBFormula(DBProp):

    expression: str = ""

    def __post_init__(self):

        self.type = PropTypes.FORMULA

    @classmethod
    def from_dict(cls: Type[DBFormula], args: dict[str, Any]) -> DBFormula:

        return DBFormula(
            name=args["name"], id=args["id"], expression=args["formula"]["expression"]
        )

    def serialize(self) -> dict[str, Any]:
        return {self.type.value: {"expression": self.expression}, "name": self.name}
