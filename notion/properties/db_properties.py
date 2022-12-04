from dataclasses import InitVar
from typing import Any
from typing import Optional

from pydantic import Field
from pydantic.dataclasses import dataclass

from notion.properties.common_properties import Option
from notion.properties.common_properties import StatusGroup
from notion.properties.prop_enums import NumberFormat
from notion.properties.prop_enums import PropTypes

# TODO: Convert from dataclass to BaseModel
# Do this once support for __post_init__ on BaseModel is released.
# Refer: https://github.com/pydantic/pydantic/issues/1729


@dataclass
class DBProp:

    name: str
    id: str = ""

    def __post_init__(self):

        self.type = PropTypes.UNSUPPORTED


class DBTitle(DBProp):
    def __post_init__(self):
        self.type = PropTypes.TITLE


class DBText(DBProp):
    def __post_init__(self):
        self.type = PropTypes.RICH_TEXT


class DBDate(DBProp):
    def __post_init__(self):
        self.type = PropTypes.DATE


class DBFiles(DBProp):
    def __post_init__(self):
        self.type = PropTypes.FILES


class DBCheckbox(DBProp):
    def __post_init__(self):
        self.type = PropTypes.CHECKBOX


class DBUrl(DBProp):
    def __post_init__(self):
        self.type = PropTypes.URL


class DBEmail(DBProp):
    def __post_init__(self):
        self.type = PropTypes.EMAIL


class DBPhoneNumber(DBProp):
    def __post_init__(self):
        self.type = PropTypes.PHONE_NUMBER


class DBCreatedTime(DBProp):
    def __post_init__(self):
        self.type = PropTypes.CREATED_TIME


class DBCreatedBy(DBProp):
    def __post_init__(self):
        self.type = PropTypes.CREATED_BY


class DBLastEditedTime(DBProp):
    def __post_init__(self):
        self.type = PropTypes.LAST_EDITED_TIME


class DBLastEditedBy(DBProp):
    def __post_init__(self):
        self.type = PropTypes.LAST_EDITED_BY


@dataclass
class DBNumber(DBProp):

    format: Optional[NumberFormat] = None
    number: InitVar[Optional[dict[str, str]]] = None

    def __post_init__(self, number: Optional[dict[str, str]]):  # type: ignore

        # Setting the format if only 'number' is given as in the
        # case of the response from the Notion API.
        if not number and not self.format:
            raise TypeError("provide 'format' or 'number'")
        if number:
            self.format = NumberFormat[number["format"].upper()]

        self.type = PropTypes.NUMBER


@dataclass
class DBSelect(DBProp):

    options: list[Option] = Field(default_factory=list)
    select: InitVar[Optional[dict[str, list[Any]]]] = None

    def __post_init__(self, select: Optional[dict[str, list[Any]]]):  # type: ignore

        if not select and not self.options:
            raise TypeError("provide 'options' or 'select'")
        if select:
            self.options = [Option(**opt) for opt in select["options"]]

        self.type = PropTypes.SELECT


@dataclass
class DBMultiSelect(DBProp):

    options: list[Option] = Field(default_factory=list)
    multi_select: InitVar[Optional[dict[str, list[Any]]]] = None

    def __post_init__(self, multi_select: Optional[dict[str, list[Any]]]):  # type: ignore

        if not multi_select and not self.options:
            raise TypeError("provide 'options' or 'select'")
        if multi_select:
            self.options = [Option(**opt) for opt in multi_select["options"]]
        self.type = PropTypes.MULTI_SELECT


@dataclass
class DBStatus(DBProp):

    options: list[Option] = Field(default_factory=list)
    groups: list[StatusGroup] = Field(default_factory=list)
    status: InitVar[Optional[dict[str, list[Any]]]] = None

    def __post_init__(self, status: Optional[dict[str, list[Any]]]):  # type: ignore

        if not status and not self.options and not self.groups:
            raise TypeError("provide 'status' or provide both 'options' and 'groups'")
        if status:
            self.options = [Option(**opt) for opt in status["options"]]
            self.groups = [StatusGroup(**grp) for grp in status["groups"]]

        self.type = PropTypes.STATUS


@dataclass
class DBFormula(DBProp):

    expression: str = ""
    formula: InitVar[Optional[dict[str, str]]] = None

    def __post_init__(self, formula: Optional[dict[str, str]]):  # type: ignore

        if not formula and not self.expression:
            raise TypeError("provide 'expression' or 'formula'")
        if formula:
            self.expression = formula["expression"]

        self.type = PropTypes.FORMULA
