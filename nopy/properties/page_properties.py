from __future__ import annotations

from dataclasses import KW_ONLY
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from typing import Any
from typing import Optional
from typing import Type
from typing import Union

import dateutil.parser as date_parser

from ..helpers import get_plain_text
from .base import BaseProperty
from .common_properties import Date
from .common_properties import File
from .common_properties import Option
from .common_properties import Text
from .prop_enums import FormulaTypes
from .prop_enums import PropTypes


@dataclass
class PProp(BaseProperty):

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


@dataclass
class PTitle(PProp):

    title: str = ""
    rich_title: list[Text] = field(default_factory=list)

    def __post_init__(self):

        self._type = PropTypes.TITLE
        self.title = get_plain_text(self.rich_title)

    @classmethod
    def from_dict(cls: Type[PTitle], args: dict[str, Any]) -> PTitle:

        rich_title = [Text.from_dict(t) for t in args["title"]]
        new_args: dict[str, Any] = {
            "name": args.get("name", ""),
            "id": args.get("id"),
            "rich_title": rich_title,
        }
        return PTitle(**new_args)


@dataclass
class PText(PProp):

    text: str = ""
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


@dataclass
class PNumber(PProp):

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


@dataclass
class PSelect(PProp):

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


@dataclass
class PMultiSelect(PProp):

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


@dataclass
class PDate(PProp):

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


@dataclass
class PFormula(PProp):

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


@dataclass
class PFile(PProp):

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


@dataclass
class PCheckbox(PProp):

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


@dataclass
class PUrl(PProp):

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


@dataclass
class PEmail(PProp):

    email: str

    def __post_init__(self):

        self._type = PropTypes.CHECKBOX

    @classmethod
    def from_dict(cls: Type[PProp], args: dict[str, Any]) -> PProp:

        new_args: dict[str, Any] = {
            "name": args.get("name", ""),
            "id": args["id"],
            "email": args["email"],
        }
        return PEmail(**new_args)


@dataclass
class PPhoneNumber(PProp):

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


@dataclass
class PCreatedTime(PProp):

    created_time: datetime

    def __post_init__(self):

        self._type = PropTypes.CREATED_TIME

    @classmethod
    def from_dict(cls: Type[PProp], args: dict[str, Any]) -> PProp:

        new_args: dict[str, Any] = {
            "name": args.get("name", ""),
            "id": args["id"],
            "created_time": date_parser.parse(args["created_time"]),
        }
        return PCreatedTime(**new_args)


@dataclass
class PLastEditedTime(PProp):

    last_edited_time: datetime

    def __post_init__(self):

        self._type = PropTypes.LAST_EDITED_TIME

    @classmethod
    def from_dict(cls: Type[PProp], args: dict[str, Any]) -> PProp:

        new_args: dict[str, Any] = {
            "name": args.get("name", ""),
            "id": args["id"],
            "last_edited_time": date_parser.parse(args["last_edited_time"]),
        }
        return PLastEditedTime(**new_args)
