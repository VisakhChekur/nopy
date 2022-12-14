from dataclasses import dataclass
from datetime import datetime
from typing import Any
from typing import ClassVar
from typing import Literal
from typing import Optional
from typing import Set
from typing import Union

from nopy.exceptions import UnsupportedError
from nopy.properties.db_properties import DBProp
from nopy.properties.prop_enums import PropTypes

Number = Union[int, float]


class TypeFilter:
    def __init__(self):

        self._type = PropTypes.UNSUPPORTED

    @property
    def type(self):
        return self._type

    def serialize(self) -> dict[str, Any]:

        if self._type == PropTypes.UNSUPPORTED:
            raise UnsupportedError("this type is unsupported")

        filters: dict[str, Any] = {}
        for attr_name, attr_val in self.__dict__.items():
            if attr_val is not None:
                filters[attr_name] = attr_val
        filters.pop("_type")

        return {self._type.value: filters}


@dataclass
class Filter:

    prop: Union[DBProp, str]
    filter: Union[TypeFilter, dict[str, Any]]

    def serialize(self) -> dict[str, Any]:

        prop_name = self.prop if not isinstance(self.prop, DBProp) else self.prop.name

        filter_dict = (
            self.filter
            if not isinstance(self.filter, TypeFilter)
            else self.filter.serialize()
        )

        serialized: dict[str, Any] = {
            "property": prop_name,
        }
        serialized.update(filter_dict)
        return serialized


@dataclass
class TextFilter(TypeFilter):

    equals: Optional[str] = None
    does_not_equal: Optional[str] = None
    contains: Optional[str] = None
    does_not_contain: Optional[str] = None
    starts_with: Optional[str] = None
    ends_with: Optional[str] = None
    is_empty: Optional[Literal[True]] = None
    is_not_empty: Optional[Literal[True]] = None

    def __post_init__(self):

        self._type = PropTypes.RICH_TEXT


@dataclass
class NumberFilter(TypeFilter):

    equals: Optional[Number] = None
    does_not_equal: Optional[Number] = None
    greater_than: Optional[Number] = None
    less_than: Optional[Number] = None
    greater_than_or_equal_to: Optional[Number] = None
    less_than_or_equal_to: Optional[Number] = None
    is_empty: Optional[Literal[True]] = None
    is_not_empty: Optional[Literal[True]] = None

    def __post_init__(self):

        self._type = PropTypes.NUMBER

    @property
    def type(self):
        return self._type


@dataclass
class CheckboxFilter(TypeFilter):

    equals: Optional[bool] = None
    does_not_equal: Optional[bool] = None

    def __post_init__(self):

        self._type = PropTypes.CHECKBOX


@dataclass
class SelectFilter(TypeFilter):

    equals: Optional[str] = None
    does_not_equal: Optional[str] = None
    is_empty: Optional[Literal[True]] = None
    is_not_empty: Optional[Literal[True]] = None

    def __post_init__(self):

        self._type = PropTypes.SELECT


@dataclass
class MultiSelectFilter(TypeFilter):

    contains: Optional[str] = None
    does_not_contains: Optional[str] = None
    is_empty: Optional[Literal[True]] = None
    is_not_empty: Optional[Literal[True]] = None

    def __post_init__(self):

        self._type = PropTypes.MULTI_SELECT


@dataclass
class StatusFilter(TypeFilter):

    equals: Optional[str] = None
    does_not_equal: Optional[str] = None
    is_empty: Optional[Literal[True]] = None
    is_not_empty: Optional[Literal[True]] = None

    def __post_init__(self):

        self._type = PropTypes.STATUS


@dataclass
class DateFilter(TypeFilter):

    # For these attributes, we can just put the value as the user provided value
    # during serialization. For the others, even if the value is 'True', the
    # value required by Notion is an empty dictionary.
    _NORMAL_ATTRS: ClassVar[Set[str]] = {
        "equals",
        "before",
        "after",
        "is_empty",
        "is_not_emtpy",
    }

    equals: Optional[datetime] = None
    before: Optional[datetime] = None
    after: Optional[datetime] = None
    on_or_before: Optional[datetime] = None
    on_or_after: Optional[datetime] = None
    past_week: Optional[Literal[True]] = None
    past_month: Optional[Literal[True]] = None
    past_year: Optional[Literal[True]] = None
    this_week: Optional[Literal[True]] = None
    next_week: Optional[Literal[True]] = None
    next_month: Optional[Literal[True]] = None
    next_year: Optional[Literal[True]] = None
    is_empty: Optional[Literal[True]] = None
    is_not_empty: Optional[Literal[True]] = None

    def __post_init__(self):

        self._type = PropTypes.DATE

    def serialize(self) -> dict[str, Any]:

        filters: dict[str, Any] = {}
        for attr_name, attr_value in self.__dict__.items():
            if attr_value is not None:
                filters[attr_name] = (
                    attr_value if attr_name in self._NORMAL_ATTRS else {}
                )

        filters.pop("_type")

        return {self._type.value: filters}


@dataclass
class FilesFilter(TypeFilter):

    is_empty: Optional[Literal[True]] = None
    is_not_empty: Optional[Literal[True]] = None

    def __post_init__(self):

        self._type = PropTypes.FILES


@dataclass
class FormulaFilter(TypeFilter):

    string: Optional[TextFilter] = None
    checkbox: Optional[CheckboxFilter] = None
    number: Optional[NumberFilter] = None
    date: Optional[DateFilter] = None

    def __post_init__(self):

        self._type = PropTypes.FORMULA

    def serialize(self) -> dict[str, Any]:

        filters: dict[str, Any] = {}
        for attr_name, attr_value in self.__dict__.items():

            if attr_value is not None and attr_name != "_type":
                attr_value: TypeFilter
                filters[attr_name] = attr_value.serialize()

        return {self._type.value: filters}
