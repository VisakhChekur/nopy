from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from typing import Any
from typing import ClassVar
from typing import Literal
from typing import Optional
from typing import Type
from typing import Union

from nopy._descriptors import TextDescriptor
from nopy.enums import PropTypes
from nopy.enums import RollupFunctions
from nopy.errors import UnsupportedByNotion
from nopy.objects.user import User
from nopy.props.base import ObjectProperty
from nopy.props.common import Date
from nopy.props.common import File
from nopy.props.common import Option
from nopy.props.common import RichText


@dataclass(eq=False)
class PCheckbox(ObjectProperty):
    """A representation of a checkbox property of a page.

    Attributes:
        id (str): The id of the property.
        name (str): The name of the property.
        checked: Whether the checkbox is checked or not.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.CHECKBOX`.
    """

    _type: ClassVar[PropTypes] = PropTypes.CHECKBOX

    checked: bool = False

    def serialize(self) -> dict[str, Any]:
        raise NotImplementedError()

    @classmethod
    def from_dict(cls: Type[PCheckbox], args: dict[str, Any]) -> PCheckbox:

        return PCheckbox(
            id=args["id"], checked=args["checkbox"], name=args.get("name", "")
        )


@dataclass(eq=False)
class PCreatedby(ObjectProperty):
    """A representation of a created by property of a page.

    Attributes:
        id (str): The id of the property.
        name (str): The name of the property.
        created_by: The user that created this page.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.CREATED_BY`.
    """

    _type: ClassVar[PropTypes] = PropTypes.CREATED_BY

    created_by: User = field(default_factory=User)

    def serialize(self) -> dict[str, Any]:

        msg = "creation/updation of created by"
        raise UnsupportedByNotion(msg)

    @classmethod
    def from_dict(cls: Type[PCreatedby], args: dict[str, Any]) -> PCreatedby:

        new_args = _get_base_page_args(args)
        new_args["created_by"] = User.from_dict(args[cls._type.value])

        return PCreatedby(**new_args)


@dataclass(eq=False)
class PCreatedTime(ObjectProperty):
    """A representation of a created time property of a page.

    Attributes:
        id (str): The id of the property.
        name (str): The name of the property.
        created_time: The time the page was created.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.CREATED_TIME`.
    """

    _type: ClassVar[PropTypes] = PropTypes.CREATED_TIME

    created_time: datetime = field(default_factory=datetime.now)

    def serialize(self) -> dict[str, Any]:

        msg = "creation/updation of created time"
        raise UnsupportedByNotion(msg)

    @classmethod
    def from_dict(cls: Type[PCreatedTime], args: dict[str, Any]) -> PCreatedTime:

        new_args = _get_base_page_args(args)
        new_args["created_time"] = datetime.fromisoformat(args[cls._type.value])

        return PCreatedTime(**new_args)


@dataclass(eq=False)
class PDate(ObjectProperty):
    """A representation of a date property of a page.

    Attributes:
        id (str): The id of the property.
        name (str): The name of the property.
        date: The date stored in the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.DATE`.
    """

    _type: ClassVar[PropTypes] = PropTypes.DATE

    date: Optional[Date] = None

    def serialize(self) -> dict[str, Any]:
        raise NotImplementedError()

    @classmethod
    def from_dict(cls: Type[PDate], args: dict[str, Any]) -> PDate:

        new_args = _get_base_page_args(args)

        date = args[cls._type.value]
        new_args["date"] = Date.from_dict(date) if date else None

        return PDate(**new_args)


@dataclass(eq=False)
class PEmail(ObjectProperty):
    """A representation of a email property of a page.

    Attributes:
        id (str): The id of the property.
        name (str): The name of the property.
        email (str): The email stored in the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.EMAIL`.
    """

    _type: ClassVar[PropTypes] = PropTypes.EMAIL

    email: Optional[str] = None

    def serialize(self) -> dict[str, Any]:
        raise NotImplementedError()

    @classmethod
    def from_dict(cls: Type[PEmail], args: dict[str, Any]) -> PEmail:

        new_args = _get_base_page_args(args)
        new_args["email"] = args["email"]

        return PEmail(**new_args)


@dataclass(eq=False)
class PFiles(ObjectProperty):
    """A representation of a files property of a page.

    Attributes:
        id (str): The id of the property.
        name (str): The name of the property.
        files: The files stored in the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.FILES`.
    """

    _type: ClassVar[PropTypes] = PropTypes.FILES

    files: list[File] = field(default_factory=list)

    def serialize(self) -> dict[str, Any]:
        raise NotImplementedError()

    @classmethod
    def from_dict(cls: Type[PFiles], args: dict[str, Any]) -> PFiles:

        new_args = _get_base_page_args(args)
        new_args["files"] = [File.from_dict(file) for file in args["files"]]

        return PFiles(**new_args)


@dataclass(eq=False)
class PFormula(ObjectProperty):
    """A representation of a formula property of a page.

    Attributes:
        id (str): The id of the property.
        name (str): The name of the property.
        value_type: The data type of the result of the calculation.
        value: The result of the calculation.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.FORMULA`.
    """

    _type: ClassVar[PropTypes] = PropTypes.FORMULA

    value_type: Literal["boolean", "date", "number", "string"] = "number"
    value: Optional[Union[bool, int, float, str, Date]] = None

    def serialize(self) -> dict[str, Any]:

        msg = "creation/updation of formula"
        raise UnsupportedByNotion(msg)

    @classmethod
    def from_dict(cls: Type[PFormula], args: dict[str, Any]) -> PFormula:

        new_args = _get_base_page_args(args)

        formula_details = args[cls._type.value]
        value_type = formula_details["type"]
        new_args["value_type"] = value_type
        new_args["value"] = formula_details[value_type]

        return PFormula(**new_args)


@dataclass(eq=False)
class PLastEditedBy(ObjectProperty):
    """A representation of a last edited by property of a page.

    Attributes:
        id (str): The id of the property.
        last_edited_by: The user that last edited this page.
        name (str): The name of the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.LAST_EDITED_BY`.
    """

    _type: ClassVar[PropTypes] = PropTypes.LAST_EDITED_BY

    last_edited_by: User = field(default_factory=User)

    def serialize(self) -> dict[str, Any]:

        msg = "creation/updation of last edited by by"
        raise UnsupportedByNotion(msg)

    @classmethod
    def from_dict(cls: Type[PLastEditedBy], args: dict[str, Any]) -> PLastEditedBy:

        new_args = _get_base_page_args(args)
        new_args["last_edited_by"] = User.from_dict(args[cls._type.value])

        return PLastEditedBy(**new_args)


@dataclass(eq=False)
class PLastEditedTime(ObjectProperty):
    """A representation of a last edited time property of a page.

    Attributes:
        id (str): The id of the property.
        name (str): The name of the property.
        last_edited_time: The time the page was last edited.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.LAST_EDITED_TIME`.
    """

    _type: ClassVar[PropTypes] = PropTypes.LAST_EDITED_TIME

    last_edited_time: datetime = field(default_factory=datetime.now)

    def serialize(self) -> dict[str, Any]:

        msg = "creation/updation of last edited time"
        raise UnsupportedByNotion(msg)

    @classmethod
    def from_dict(cls: Type[PLastEditedTime], args: dict[str, Any]) -> PLastEditedTime:

        new_args = _get_base_page_args(args)
        new_args["last_edited_time"] = datetime.fromisoformat(args[cls._type.value])

        return PLastEditedTime(**new_args)


@dataclass(eq=False)
class PMultiselect(ObjectProperty):
    """A representation of a multi select property of a page.

    Attributes:
        id (str): The id of the property.
        name (str): The name of the property.
        options: The selected options.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.MULTI_SELECT`.
    """

    _type: ClassVar[PropTypes] = PropTypes.MULTI_SELECT

    options: list[Option] = field(default_factory=list)

    def serialize(self) -> dict[str, Any]:
        raise NotImplementedError()

    @classmethod
    def from_dict(cls: Type[PMultiselect], args: dict[str, Any]) -> PMultiselect:

        new_args = _get_base_page_args(args)
        new_args["options"] = [Option.from_dict(opt) for opt in args[cls._type.value]]

        return PMultiselect(**new_args)


@dataclass(eq=False)
class PNumber(ObjectProperty):
    """A representation of a number property of a page.

    Attributes:
        id (str): The id of the property.
        name (str): The name of the property.
        number: The number stored in the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.NUMBER`.
    """

    _type: ClassVar[PropTypes] = PropTypes.NUMBER

    number: Optional[Union[int, float]] = None

    def serialize(self) -> dict[str, Any]:
        raise NotImplementedError()

    @classmethod
    def from_dict(cls: Type[PNumber], args: dict[str, Any]) -> PNumber:

        new_args = _get_base_page_args(args)
        new_args["number"] = args[cls._type.value]

        return PNumber(**new_args)


@dataclass(eq=False)
class PPeople(ObjectProperty):
    """A representation of a people property of a page.

    Attributes:
        id (str): The id of the property.
        name (str): The name of the property.
        people: The people.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.PEOPLE`.
    """

    _type: ClassVar[PropTypes] = PropTypes.PEOPLE

    people: list[User] = field(default_factory=list)

    def serialize(self) -> dict[str, Any]:
        raise NotImplementedError()

    @classmethod
    def from_dict(cls: Type[PPeople], args: dict[str, Any]) -> PPeople:

        new_args = _get_base_page_args(args)
        new_args["people"] = [User.from_dict(user) for user in args[cls._type.value]]

        return PPeople(**new_args)


@dataclass(eq=False)
class PPhonenumber(ObjectProperty):
    """A representation of a phone number property of a page.

    Attributes:
        id (str): The id of the property.
        name (str): The name of the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.PHONE_NUMBER`.
    """

    _type: ClassVar[PropTypes] = PropTypes.PHONE_NUMBER

    phone_number: Optional[str] = None

    def serialize(self) -> dict[str, Any]:
        raise NotImplementedError()

    @classmethod
    def from_dict(cls: Type[PPhonenumber], args: dict[str, Any]) -> PPhonenumber:

        new_args = _get_base_page_args(args)
        new_args["phone_number"] = args[cls._type.value]

        return PPhonenumber(**new_args)


@dataclass(eq=False)
class PRelation(ObjectProperty):
    """A representation of a relation property of a page.

    Attributes:
        id (str): The id of the property.
        name (str): The name of the property.
        relations: The ids of the pages this property relates to.
        has_more:
            Denotes whether there are more relations. If `True`, to get
            the rest of the relations, use the `retrieve_prop` method
            on the instance of a `Page`.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.RELATION`.
    """

    _type: ClassVar[PropTypes] = PropTypes.RELATION

    relations: list[str] = field(default_factory=list)
    has_more: bool = False

    def serialize(self) -> dict[str, Any]:
        raise NotImplementedError()

    @classmethod
    def from_dict(cls: Type[PRelation], args: dict[str, Any]) -> PRelation:

        new_args = _get_base_page_args(args)

        new_args["has_more"] = args["has_more"]
        new_args["relations"] = [relation_["id"] for relation_ in args[cls._type.value]]

        return PRelation(**new_args)


@dataclass(eq=False)
class PRollup(ObjectProperty):
    """A representation of a rollup property of a page.

    Attributes:
        id (str): The id of the property.
        name (str): The name of the property.
        value_type: The type the result of the calculation is.
        value: The result of the calculation.
        function: The function which is used for the calculation.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.ROLLUP`.
    """

    _type: ClassVar[PropTypes] = PropTypes.ROLLUP

    value_type: Literal[
        "number", "date", "array", "unsupported", "incomplete"
    ] = "number"
    value: Union[int, float, Date, list[Any]] = 0
    function: RollupFunctions = RollupFunctions.COUNT

    def serialize(self) -> dict[str, Any]:
        raise NotImplementedError()

    @classmethod
    def from_dict(cls: Type[PRollup], args: dict[str, Any]) -> PRollup:

        new_args = _get_base_page_args(args)

        rollup_details = args[cls._type.value]
        rollup = {
            "value_type": rollup_details["type"],
            "value": rollup_details[rollup_details["type"]],
            "function": RollupFunctions[rollup_details["function"].upper()],
        }

        return PRollup(**new_args, **rollup)


@dataclass(eq=False)
class PRichtext(ObjectProperty):
    """A representation of a rich text property of a page.

    Attributes:
        id (str): The id of the property.
        name (str): The name of the property.\
        text (str): The text without styling.
        rich_text: The text with styling.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.RICH_TEXT`.
    """

    _type: ClassVar[PropTypes] = PropTypes.RICH_TEXT
    text: ClassVar[TextDescriptor] = TextDescriptor("rich_text")

    rich_text: list[RichText] = field(default_factory=list)

    def serialize(self) -> dict[str, Any]:
        raise NotImplementedError()

    @classmethod
    def from_dict(cls: Type[PRichtext], args: dict[str, Any]) -> PRichtext:

        new_args = _get_base_page_args(args)
        new_args["rich_text"] = [RichText.from_dict(rt) for rt in args[cls._type.value]]

        return PRichtext(**new_args)


@dataclass(eq=False)
class PSelect(ObjectProperty):
    """A representation of a select property of a page.

    Attributes:
        id (str): The id of the property.
        name (str): The name of the property.
        option: The selected option, if any.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.SELECT`.
    """

    _type: ClassVar[PropTypes] = PropTypes.SELECT

    option: Optional[Option] = None

    def serialize(self) -> dict[str, Any]:
        raise NotImplementedError()

    @classmethod
    def from_dict(cls: Type[PSelect], args: dict[str, Any]) -> PSelect:

        new_args: dict[str, Any] = _get_base_page_args(args)

        option = args[cls._type.value]
        new_args["option"] = Option.from_dict(option) if option else None

        return PSelect(**new_args)


@dataclass(eq=False)
class PStatus(ObjectProperty):
    """A representation of a status property of a page.

    Attributes:
        id (str): The id of the property.
        name (str): The name of the property.
        status: The selected status, if any.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.STATUS`.
    """

    _type: ClassVar[PropTypes] = PropTypes.STATUS

    status: Optional[Option] = None

    def serialize(self) -> dict[str, Any]:
        raise NotImplementedError()

    @classmethod
    def from_dict(cls: Type[PStatus], args: dict[str, Any]) -> PStatus:

        new_args = _get_base_page_args(args)
        new_args["status"] = Option.from_dict(args[cls._type.value])

        return PStatus(**new_args)


@dataclass(eq=False)
class PUrl(ObjectProperty):
    """A representation of a url property of a page.

    Attributes:
        id (str): The id of the property.
        name (str): The name of the property.
        url: The URL.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.URL`.
    """

    _type: ClassVar[PropTypes] = PropTypes.URL

    url: Optional[str] = None

    def serialize(self) -> dict[str, Any]:
        raise NotImplementedError()

    @classmethod
    def from_dict(cls: Type[PUrl], args: dict[str, Any]) -> PUrl:

        new_args = _get_base_page_args(args)
        new_args["url"] = args[cls._type.value]

        return PUrl(**new_args)


# ----- Helper for `from_dict` -----
def _get_base_page_args(args: dict[str, Any]) -> dict[str, Any]:

    return {"id": args["id"], "name": args.get("name", "")}
