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
from nopy.props.base import ObjectProperty
from nopy.props.common import Option
from nopy.props.common import StatusGroup


@dataclass(eq=False)
class DBText(ObjectProperty):
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
class DBNumber(ObjectProperty):
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
    def from_dict(cls: Type[ObjectProperty], args: dict[str, Any]) -> ObjectProperty:

        format = args[DBNumber._type.value]["format"]
        return DBNumber(
            id=args["id"], name=args["name"], format=NumberFormat[format.upper()]
        )


@dataclass(eq=False)
class DBSelect(ObjectProperty):
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


@dataclass(eq=False)
class DBStatus(ObjectProperty):
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


@dataclass(eq=False)
class DBMultiSelect(ObjectProperty):
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


@dataclass(eq=False)
class DBDate(ObjectProperty):
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
class DBPeople(ObjectProperty):
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
class DBFiles(ObjectProperty):
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
class DBCheckbox(ObjectProperty):
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
class DBUrl(ObjectProperty):
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
class DBEmail(ObjectProperty):
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
class DBPhoneNumber(ObjectProperty):
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
class DBFormula(ObjectProperty):
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
    def from_dict(cls: Type[ObjectProperty], args: dict[str, Any]) -> ObjectProperty:

        return DBFormula(
            name=args["name"],
            id=args["id"],
            expression=args[DBFormula._type.value]["expression"],
        )


@dataclass(eq=False)
class DBRelation(ObjectProperty):
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


@dataclass(eq=False)
class DBRollup(ObjectProperty):
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
    def from_dict(cls: Type[ObjectProperty], args: dict[str, Any]) -> ObjectProperty:

        rollup_details = args[DBRollup._type.value]
        return DBRollup(id=args["id"], name=args["name"], **rollup_details)


@dataclass(eq=False)
class DBCreatedTime(ObjectProperty):
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
class DBCreatedBy(ObjectProperty):
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
class DBLastEditedTime(ObjectProperty):
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
class DBLastEditedBy(ObjectProperty):
    """A representation of a last edited by property on a database.

    Attributes:

        id (str): The id of the property.
        name (str): The name of the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.LAST_EDITED_BY`.
    """

    _type: ClassVar[PropTypes] = PropTypes.LAST_EDITED_BY
