from __future__ import annotations

from dataclasses import KW_ONLY
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from typing import Any
from typing import ClassVar
from typing import Optional
from typing import Type
from typing import Union

from ..enums import FormulaTypes
from ..enums import PropTypes
from ..helpers import TextDescriptor
from ..helpers import get_plain_text
from .base import BaseProperty
from .common_properties import Date
from .common_properties import File
from .common_properties import Option
from .common_properties import Text


@dataclass(eq=False)
class PProp(BaseProperty):
    """The base property from which all page properties inherit.

    Attributes:
        name (str): The name of the property.
        id (str): The id of the property.
        type (PropTyes):
            The type of the property which will always be
            `PropTyes.UNSUPPORTED`.
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
    def from_dict(cls: Type[PProp], args: dict[str, Any]) -> PProp:

        # NOTE: "name" is not required as per the Notion specification
        # but it is included if given to make life easier for the user
        new_args: dict[str, Any] = {"name": args.get("name", ""), "id": args.get("id")}
        return PProp(**new_args)


@dataclass(eq=False)
class PTitle(PProp):
    """A representation of a 'Title' page property.

    Attributes:
        name (str): The name of the property.
        title (str): The title as plain text.
        rich_title (list[Text]): The title with the styling information.
        id (str): The id of the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.TITLE`.
    """

    title: ClassVar[TextDescriptor] = TextDescriptor("rich_title")

    rich_title: list[Text] = field(default_factory=list)

    def __post_init__(self):

        self._type = PropTypes.TITLE

    @classmethod
    def from_dict(cls: Type[PTitle], args: dict[str, Any]) -> PTitle:

        rich_title = [Text.from_dict(t) for t in args["title"]]
        new_args: dict[str, Any] = {
            "name": args.get("name", ""),
            "id": args.get("id"),
            "rich_title": rich_title,
        }
        return PTitle(**new_args)


@dataclass(eq=False)
class PText(PProp):
    """A representation of a 'Text' page property.

    Attributes:
        name (str): The name of the property.
        text (str):  The text as plain text.
        rich_text (list[Text]): The text with the styling information.
        id (str): The id of the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.TEXT`.
    """

    text: ClassVar[TextDescriptor] = TextDescriptor("rich_text")

    rich_text: list[Text] = field(default_factory=list)

    def __post_init__(self):

        self._type = PropTypes.RICH_TEXT
        self.text = get_plain_text(self.rich_text)

    @classmethod
    def from_dict(cls: Type[PText], args: dict[str, Any]) -> PText:

        rich_text = [Text.from_dict(t) for t in args["rich_text"]]
        new_args: dict[str, Any] = {
            "name": args.get("name", ""),
            "id": args.get("id"),
            "rich_text": rich_text,
        }
        return PText(**new_args)


@dataclass(eq=False)
class PCheckbox(PProp):
    """A representation of a 'Checkbox' page property.

    Attributes:
        name (str): The name of the property.
        checked (bool): Whether the checkbox is checked or not.
        id (str): The id of the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.CHECKBOX`.
    """

    checked: bool

    def __post_init__(self):

        self._type = PropTypes.CHECKBOX

    @classmethod
    def from_dict(cls: Type[PProp], args: dict[str, Any]) -> PProp:

        new_args: dict[str, Any] = {
            "name": args.get("name", ""),
            "id": args["id"],
            "checked": args["checkbox"],
        }
        return PCheckbox(**new_args)


@dataclass(eq=False)
class PDate(PProp):
    """A representation of a 'Date' page property.

    Attributes:
        name (str): The name of the property.
        date (Date): The date.
        id (str): The id of the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.DATE`.
    """

    date: Date

    def __post_init__(self):

        self._type = PropTypes.DATE

    @classmethod
    def from_dict(cls: Type[PProp], args: dict[str, Any]) -> PProp:

        new_args: dict[str, Any] = {
            "name": args.get("name", ""),
            "id": args["id"],
            "date": Date.from_dict(args["date"]),
        }
        return PDate(**new_args)


@dataclass(eq=False)
class PEmail(PProp):
    """A representation of a 'Email' page property.

    Attributes:
        name (str): The name of the property.
        email (str): The email id.
        id (str): The id of the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.EMAIL`.
    """

    email: str

    def __post_init__(self):

        self._type = PropTypes.EMAIL

    @classmethod
    def from_dict(cls: Type[PProp], args: dict[str, Any]) -> PProp:

        new_args: dict[str, Any] = {
            "name": args.get("name", ""),
            "id": args["id"],
            "email": args["email"],
        }
        return PEmail(**new_args)


@dataclass(eq=False)
class PFile(PProp):
    """A representation of a 'File' page property.

    Attributes:
        name (str): The name of the property.
        files (list[File]): The list of files being stored.
        id (str): The id of the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.FILE`.
    """

    files: list[File] = field(default_factory=list)

    def __post_init__(self):

        self._type = PropTypes.FILES

    @classmethod
    def from_dict(cls: Type[PProp], args: dict[str, Any]) -> PProp:

        new_args: dict[str, Any] = {
            "name": args.get("name", ""),
            "id": args["id"],
            "files": [File.from_dict(f) for f in args["files"]],
        }

        return PFile(**new_args)


@dataclass(eq=False)
class PFormula(PProp):
    """A representation of a 'Formula' page property.

    Attributes:
        name (str): The name of the property.
        value (Union[str, float, bool, Date]):
            The actual value as calculated via the formula.
        formula_type (FormulaTypes): The type of the formula.
        id (str): The id of the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.FORMULA`.
    """

    value: Union[str, float, bool, Date]
    formula_type: FormulaTypes = FormulaTypes.NUMBER

    def __post_init__(self):

        self._type = PropTypes.FORMULA

    @classmethod
    def from_dict(cls: Type[PProp], args: dict[str, Any]) -> PProp:

        formula_type = FormulaTypes[args["formula"]["type"].upper()]
        new_args: dict[str, Any] = {
            "name": args.get("name", ""),
            "id": args["id"],
            "formula_type": formula_type,
        }

        if formula_type == FormulaTypes.STRING:
            new_args["value"] = args["formula"]["string"]
        elif formula_type == FormulaTypes.NUMBER:
            new_args["value"] = args["formula"]["number"]
        elif formula_type == FormulaTypes.BOOLEAN:
            new_args["value"] = args["formula"]["boolean"]
        else:
            new_args["value"] = Date.from_dict(args["formula"]["date"])

        return PFormula(**new_args)


@dataclass(eq=False)
class PNumber(PProp):
    """A representation of a 'Number' page property.

    Attributes:
        name (str): The name of the property.
        number (float): The number being stored.
        id (str): The id of the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.NUMBER`.
    """

    number: float = 0

    def __post_init__(self):

        self._type = PropTypes.NUMBER

    @classmethod
    def from_dict(cls: Type[PNumber], args: dict[str, Any]) -> PNumber:

        new_args: dict[str, Any] = {
            "name": args.get("name", ""),
            "id": args["id"],
            "number": args["number"],
        }
        return PNumber(**new_args)


@dataclass(eq=False)
class PPhoneNumber(PProp):
    """A representation of a 'PhoneNumber' page property.

    Attributes:
        name (str): The name of the property.
        phone_number (str): The phone number being stored.
        id (str): The id of the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.PHONE_NUMBER`.
    """

    phone_number: str

    def __post_init__(self):

        self._type = PropTypes.PHONE_NUMBER

    @classmethod
    def from_dict(cls: Type[PProp], args: dict[str, Any]) -> PProp:

        new_args: dict[str, Any] = {
            "name": args.get("name", ""),
            "id": args["id"],
            "phone_number": args["phone_number"],
        }
        return PPhoneNumber(**new_args)


@dataclass(eq=False)
class PSelect(PProp):
    """A representation of a 'Select' page property.

    Attributes:
        name (str): The name of the property.
        option (Optional[Option]):
            The selected option. If no option is selected, the it's `None`.
        id (str): The id of the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.SELECT`.
    """

    option: Optional[Option] = None

    def __post_init__(self):

        self._type = PropTypes.SELECT

    @classmethod
    def from_dict(cls: Type[PSelect], args: dict[str, Any]) -> PSelect:

        option = Option.from_dict(args["select"]) if args["select"] else None
        new_args: dict[str, Any] = {
            "name": args.get("name", ""),
            "id": args["id"],
            "option": option,
        }
        return PSelect(**new_args)


@dataclass(eq=False)
class PMultiSelect(PProp):
    """A representation of a 'MultiSelect' page property.

    Attributes:
        name (str): The name of the property.
        options (list[Option]):
            The list of selected options. If not options are selected,
            then it's an empty list.
        id (str): The id of the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.MULTI_SELECT`.
    """

    options: list[Option] = field(default_factory=list)

    def __post_init__(self):

        self._type = PropTypes.MULTI_SELECT

    @classmethod
    def from_dict(cls: Type[PMultiSelect], args: dict[str, Any]) -> PMultiSelect:

        if args["multi_select"]:
            options = [Option.from_dict(opt) for opt in args["multi_select"]]
        else:
            options = []
        new_args: dict[str, Any] = {
            "name": args.get("name", ""),
            "id": args["id"],
            "options": options,
        }
        return PMultiSelect(**new_args)


@dataclass(eq=False)
class PUrl(PProp):
    """A representation of a 'Url' page property.

    Attributes:
        name (str): The name of the property.
        url (str): The URL being stored.
        id (str): The id of the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.URL`.
    """

    url: str

    def __post_init__(self):

        self._type = PropTypes.URL

    @classmethod
    def from_dict(cls: Type[PProp], args: dict[str, Any]) -> PProp:

        new_args: dict[str, Any] = {
            "name": args.get("name", ""),
            "id": args["id"],
            "url": args["url"],
        }
        return PUrl(**new_args)


@dataclass(eq=False)
class PCreatedTime(PProp):
    """A representation of a 'CreatedTime' page property.

    Attributes:
        name (str): The name of the property.
        created_time (datetime): The created time.
        id (str): The id of the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.CREATED_TIME`.
    """

    created_time: datetime

    def __post_init__(self):

        self._type = PropTypes.CREATED_TIME

    @classmethod
    def from_dict(cls: Type[PProp], args: dict[str, Any]) -> PProp:

        new_args: dict[str, Any] = {
            "name": args.get("name", ""),
            "id": args["id"],
            "created_time": datetime.fromisoformat(args["created_time"]),
        }
        return PCreatedTime(**new_args)


@dataclass(eq=False)
class PLastEditedTime(PProp):
    """A representation of a 'LastEditedTime' page property.

    Attributes:
        name (str): The name of the property.
        last_edited_time (datetime): The last edited time.
        id (str): The id of the property.
        type (PropTypes):
            The type of the property which will always be
            `PropTypes.LAST_EDITED_TIME`.
    """

    last_edited_time: datetime

    def __post_init__(self):

        self._type = PropTypes.LAST_EDITED_TIME

    @classmethod
    def from_dict(cls: Type[PProp], args: dict[str, Any]) -> PProp:

        new_args: dict[str, Any] = {
            "name": args.get("name", ""),
            "id": args["id"],
            "last_edited_time": datetime.fromisoformat(args["last_edited_time"]),
        }
        return PLastEditedTime(**new_args)
