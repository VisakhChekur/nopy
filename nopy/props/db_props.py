"""All the database properties."""
from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import ClassVar
from typing import Literal
from typing import Optional
from typing import Type

from nopy.enums import NumberFormat
from nopy.enums import PropTypes
from nopy.enums import RollupFunctions
from nopy.errors import SerializationError
from nopy.errors import UnsupportedByNotion
from nopy.props.base import ObjectProperty
from nopy.props.common import Option
from nopy.props.common import StatusGroup


@dataclass(eq=False)
class DBProp(ObjectProperty):
    def serialize(self) -> dict[str, Any]:

        if self._type == PropTypes.UNSUPPORTED:
            return super().serialize()

        return {self._type.value: {}, "name": self.name}


@dataclass(eq=False)
class DBText(DBProp):
    """A representation of a 'Text' property on a database.

    Attributes:
        id (str): The id of the property.
        name (str): The name of the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.RICH_TEXT`.
    """

    _type: ClassVar[PropTypes] = PropTypes.RICH_TEXT


@dataclass(eq=False)
class DBNumber(DBProp):
    """A representation of a number property on a database.

    Attributes:

        id (str): The id of the property.
        name (str): The name of the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.NUMBER`.
    """

    _type: ClassVar[PropTypes] = PropTypes.NUMBER

    format: NumberFormat = NumberFormat.NUMBER

    @classmethod
    def from_dict(cls: Type[DBNumber], args: dict[str, Any]) -> DBNumber:

        format = args[DBNumber._type.value]["format"]
        return DBNumber(
            id=args["id"], name=args["name"], format=NumberFormat[format.upper()]
        )


@dataclass(eq=False)
class DBSelect(DBProp):
    """A representation of a select property on a database.

    Attributes:

        id (str): The id of the property.
        name (str): The name of the property.
        options: The select options.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.SELECT`.
    """

    _type: ClassVar[PropTypes] = PropTypes.SELECT

    options: list[Option] = field(default_factory=list)

    @classmethod
    def from_dict(cls: Type[DBSelect], args: dict[str, Any]) -> DBSelect:

        options = [Option.from_dict(rt) for rt in args[DBSelect._type.value]["options"]]
        return DBSelect(name=args["name"], id=args["id"], options=options)

    def serialize(self) -> dict[str, Any]:

        return {
            self._type.value: {"options": [opt.serialize() for opt in self.options]}
        }


@dataclass(eq=False)
class DBStatus(DBProp):
    """A representation of a status property on a database.

    Attributes:

        id (str): The id of the property.
        name (str): The name of the property.
        options: The select options.
        groups: The available groups.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.STATUS`.
    """

    _type: ClassVar[PropTypes] = PropTypes.STATUS

    options: list[Option] = field(default_factory=list)
    groups: list[StatusGroup] = field(default_factory=list)

    @classmethod
    def from_dict(cls: Type[DBStatus], args: dict[str, Any]) -> DBStatus:

        status_details = args[DBStatus._type.value]
        options = [Option.from_dict(rt) for rt in status_details["options"]]
        groups = [StatusGroup.from_dict(grp) for grp in status_details["groups"]]
        return DBStatus(
            name=args["name"], id=args["id"], options=options, groups=groups
        )

    def serialize(self) -> dict[str, Any]:

        msg = "creating/updating status via the API"
        raise UnsupportedByNotion(msg)


@dataclass(eq=False)
class DBMultiSelect(DBProp):
    """A representation of a multi select property on a database.

    Attributes:

        id (str): The id of the property.
        name (str): The name of the property.
        options: The select options.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.MULTI_SELECT`.
    """

    _type: ClassVar[PropTypes] = PropTypes.MULTI_SELECT

    options: list[Option] = field(default_factory=list)

    @classmethod
    def from_dict(cls: Type[DBMultiSelect], args: dict[str, Any]) -> DBMultiSelect:

        options = [
            Option.from_dict(rt) for rt in args[DBMultiSelect._type.value]["options"]
        ]
        return DBMultiSelect(name=args["name"], id=args["id"], options=options)

    def serialize(self) -> dict[str, Any]:
        return {
            self._type.value: {"options": [opt.serialize() for opt in self.options]}
        }


@dataclass(eq=False)
class DBDate(DBProp):
    """A representation of a date property on a database.

    Attributes:

        id (str): The id of the property.
        name (str): The name of the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.DATE`.
    """

    _type: ClassVar[PropTypes] = PropTypes.DATE


@dataclass(eq=False)
class DBPeople(DBProp):
    """A representation of a people property on a database.

    Attributes:

        id (str): The id of the property.
        name (str): The name of the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.PEOPLE`.
    """

    _type: ClassVar[PropTypes] = PropTypes.PEOPLE


@dataclass(eq=False)
class DBFiles(DBProp):
    """A representation of a files property on a database.

    Attributes:

        id (str): The id of the property.
        name (str): The name of the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.FILES`.
    """

    _type: ClassVar[PropTypes] = PropTypes.FILES


@dataclass(eq=False)
class DBCheckbox(DBProp):
    """A representation of a checkbox property on a database.

    Attributes:

        id (str): The id of the property.
        name (str): The name of the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.CHECKBOX`.
    """

    _type: ClassVar[PropTypes] = PropTypes.CHECKBOX


@dataclass(eq=False)
class DBUrl(DBProp):
    """A representation of a url property on a database.

    Attributes:

        id (str): The id of the property.
        name (str): The name of the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.URL`.
    """

    _type: ClassVar[PropTypes] = PropTypes.URL


@dataclass(eq=False)
class DBEmail(DBProp):
    """A representation of a email property on a database.

    Attributes:

        id (str): The id of the property.
        name (str): The name of the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.EMAIL`.
    """

    _type: ClassVar[PropTypes] = PropTypes.EMAIL


@dataclass(eq=False)
class DBPhoneNumber(DBProp):
    """A representation of a phone number property on a database.

    Attributes:

        id (str): The id of the property.
        name (str): The name of the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.PHONE_NUMBER`.
    """

    _type: ClassVar[PropTypes] = PropTypes.PHONE_NUMBER


@dataclass(eq=False)
class DBFormula(DBProp):
    """A representation of a formula property on a database.

    Attributes:

        id (str): The id of the property.
        name (str): The name of the property.
        expression: The expression used to evaluate the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.FORMULA`.
    """

    _type: ClassVar[PropTypes] = PropTypes.FORMULA

    expression: str = ""

    @classmethod
    def from_dict(cls: Type[DBFormula], args: dict[str, Any]) -> DBFormula:

        return DBFormula(
            name=args["name"],
            id=args["id"],
            expression=args[DBFormula._type.value]["expression"],
        )


@dataclass(eq=False)
class DBRelation(DBProp):
    """A representation of a relation property on a database.

    Attributes:

        id (str): The id of the property.
        name (str): The name of the property.
        database_id: The id of the database it's related to.
        relation_type: The relation type.
        synced_property_name: The name of the property it's synced with.
        synced_property_id: The id of the property it's synced with.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.RELATION`.
    """

    _type: ClassVar[PropTypes] = PropTypes.RELATION

    database_id: str = ""
    relation_type: Literal["single_property", "dual_property"] = "single_property"
    synced_property_name: Optional[str] = None
    synced_property_id: Optional[str] = None

    @classmethod
    def from_dict(cls: Type[DBRelation], args: dict[str, Any]) -> DBRelation:

        # This is some trash code, but it works.
        relation = args[DBRelation._type.value]
        relation_type = relation.pop("type")
        details = relation.pop(relation_type)
        relation.update(details)
        relation["relation_type"] = relation_type

        return DBRelation(id=args["id"], name=args["name"], **relation)

    def serialize(self) -> dict[str, Any]:

        if not self.database_id:
            raise SerializationError("database_id must be provided", self)

        return {
            self._type.value: {
                "database_id": self.database_id,
                "type": self.relation_type,
                self.relation_type: {},
            },
            "name": self.name,
        }


@dataclass(eq=False)
class DBRollup(DBProp):
    """A representation of a rollup property on a database.

    Attributes:

        id (str): The id of the property.
        name (str): The name of the property.
        relation_prop_name:
            The name of the relation property this property is responsible
            for rolling up.
        relation_id_name:
            The id of the relation property this property is responsible
            for rolling up.
        rollup_property_name:
            The name of the property of the pages in the related
            database.
        rollup_property_id:
            The id of the property of the pages in the related
            database.
        function:
            The function that's evaluated for every page
            in the relation of the rollup.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.ROLLUP`.
    """

    _type: ClassVar[PropTypes] = PropTypes.ROLLUP

    relation_property_name: str = ""
    relation_property_id: str = ""
    rollup_property_name: str = ""
    rollup_property_id: str = ""
    function: RollupFunctions = RollupFunctions.COUNT

    @classmethod
    def from_dict(cls: Type[DBRollup], args: dict[str, Any]) -> DBRollup:

        rollup_details = args[DBRollup._type.value]
        rollup_details["function"] = RollupFunctions[rollup_details["function"].upper()]
        return DBRollup(id=args["id"], name=args["name"], **rollup_details)

    def serialize(self) -> dict[str, Any]:

        rollup_details: dict[str, Any] = {"function": self.function.value}

        if self.relation_property_id:
            rollup_details["relation_property_id"] = self.relation_property_id
        elif self.relation_property_name:
            rollup_details["relation_property_name"] = self.relation_property_name
        else:
            msg = (
                "one of relation_property_name or relation_property_id must be provided"
            )
            raise SerializationError(msg, self)

        if self.rollup_property_id:
            rollup_details["rollup_property_id"] = self.rollup_property_id
        elif self.rollup_property_name:
            rollup_details["rollup_property_name"] = self.rollup_property_name
        else:
            msg = "one of rollup_property_name or rollup_property_id must be provided"
            raise SerializationError(msg, self)

        return {self._type.value: rollup_details, "name": self.name}


@dataclass(eq=False)
class DBCreatedTime(DBProp):
    """A representation of a created time property on a database.

    Attributes:

        id (str): The id of the property.
        name (str): The name of the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.CREATED_TIME`.
    """

    _type: ClassVar[PropTypes] = PropTypes.CREATED_TIME


@dataclass(eq=False)
class DBCreatedBy(DBProp):
    """A representation of a created by property on a database.

    Attributes:

        id (str): The id of the property.
        name (str): The name of the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.CREATED_BY`.
    """

    _type: ClassVar[PropTypes] = PropTypes.CREATED_BY


@dataclass(eq=False)
class DBLastEditedTime(DBProp):
    """A representation of a last edited time property on a database.

    Attributes:

        id (str): The id of the property.
        name (str): The name of the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.LAST_EDITED_TIME`.
    """

    _type: ClassVar[PropTypes] = PropTypes.LAST_EDITED_TIME


@dataclass(eq=False)
class DBLastEditedBy(DBProp):
    """A representation of a last edited by property on a database.

    Attributes:

        id (str): The id of the property.
        name (str): The name of the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.LAST_EDITED_BY`.
    """

    _type: ClassVar[PropTypes] = PropTypes.LAST_EDITED_BY
