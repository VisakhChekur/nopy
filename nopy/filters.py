from dataclasses import dataclass
from datetime import datetime
from typing import Any
from typing import ClassVar
from typing import Literal
from typing import Optional
from typing import Set
from typing import Union

from nopy.enums import PropTypes
from nopy.errors import UnuspportedError
from nopy.types import DBProps

Number = Union[int, float]


class PropFilter:
    def __init__(self):

        self._type = PropTypes.UNSUPPORTED

    @property
    def type(self):
        return self._type

    def serialize(self) -> dict[str, Any]:

        if self._type == PropTypes.UNSUPPORTED:
            raise UnuspportedError("this type is unsupported")

        filters: dict[str, Any] = {}
        for attr_name, attr_val in self.__dict__.items():
            if attr_val is not None:
                filters[attr_name] = attr_val
        filters.pop("_type")

        return {self._type.value: filters}


@dataclass
class Filter:
    """A filter object.

    Attributes:
        prop: The property or the id of the property to filter.
        filter: The filter to apply on the property.
    """

    prop: Union[DBProps, str]
    filter: Union[PropFilter, dict[str, Any]]

    def serialize(self) -> dict[str, Any]:

        prop_name = self.prop if not isinstance(self.prop, DBProps) else self.prop.name

        filter_dict = (
            self.filter
            if not isinstance(self.filter, PropFilter)
            else self.filter.serialize()
        )

        serialized: dict[str, Any] = {
            "property": prop_name,
        }
        serialized.update(filter_dict)
        return serialized


@dataclass
class TextFilter(PropFilter):
    """A filter for text properties.

    Attributes:
        equals: Property value is an exact match.
        does_not_equal: Property value does not match exactly.
        contains: Property value contains the string.
        does_not_contain: Property value does not contain the string.
        starts_with: Property value start with the string.
        ends_with: Property value ends with the string.
        is_empty: Property value is empty.
        is_not_empty: Property value is not empty.
    """

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
class NumberFilter(PropFilter):
    """A filter for number properties.

    Attributes:
        equals: Property value is an exact match.
        does_not_equal: Property value is not an exact match.
        greater_than: Property value is greater than the number.
        less_than: Property value is less than the number.
        greater_than_or_equal_to: Property value is greater than or
            equal to the number.
        less_than_or_equal_to: Property value is less than or equal
            to the the number.
        is_empty: Property value is empty.
        is_not_empty: Property value is not empty.
    """

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
class CheckboxFilter(PropFilter):
    """A filter for checkbox properties.

    Attributes:
        equals: Property value matches the boolean.
        does_not_equal: Property value does not match the boolean.
    """

    equals: Optional[bool] = None
    does_not_equal: Optional[bool] = None

    def __post_init__(self):

        self._type = PropTypes.CHECKBOX


@dataclass
class SelectFilter(PropFilter):
    """A filter for a select property.

    Attributes:
        equals: Property value matches the string.
        does_not_equal: Property value does not match the string.
        is_empty: Property value is empty.
        is_not_empty: Property value is not empty.
    """

    equals: Optional[str] = None
    does_not_equal: Optional[str] = None
    is_empty: Optional[Literal[True]] = None
    is_not_empty: Optional[Literal[True]] = None

    def __post_init__(self):

        self._type = PropTypes.SELECT


@dataclass
class MultiSelectFilter(PropFilter):
    """A filter for a multi select property.

    Attributes:
        contains: Property value contains the string.
        does_not_contains: Property value does not contain the string.
        is_empty: Property value is empty.
        is_not_empty: Property value is not empty.
    """

    contains: Optional[str] = None
    does_not_contains: Optional[str] = None
    is_empty: Optional[Literal[True]] = None
    is_not_empty: Optional[Literal[True]] = None

    def __post_init__(self):

        self._type = PropTypes.MULTI_SELECT


@dataclass
class StatusFilter(PropFilter):
    """A filter for a status property.

    Attributes:
        equals: Property value matches the string.
        does_not_equal: Property value does not match the string.
        is_empty: Property value is empty.
        is_not_empty: Property value is not empty.
    """

    equals: Optional[str] = None
    does_not_equal: Optional[str] = None
    is_empty: Optional[Literal[True]] = None
    is_not_empty: Optional[Literal[True]] = None

    def __post_init__(self):

        self._type = PropTypes.STATUS


@dataclass
class DateFilter(PropFilter):
    """A filter for date properties.

    Attributes:
        equals: The property value equals the date.
        before: The property value is before the date.
        after: The property value is after the date.
        on_or_before: The property value is on or before the date.
        on_or_after: The property value is on or after the date.
        past_week: The property value is within the past week.
        past_month: The property value is within the past month.
        past_year: The property value is within the past year.
        this_week: The property value is within this week.
        next_week: The property value is within next week.
        next_month: The property value is within next month.
        next_year: The property value is within next year.
        is_empty: Property value is empty.
        is_not_empty: Property value is not empty.
    """

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
class FilesFilter(PropFilter):
    """A filter for files properties.

    Attributes:
        is_empty: Property value is empty.
        is_not_empty: Property value is not empty.
    """

    is_empty: Optional[Literal[True]] = None
    is_not_empty: Optional[Literal[True]] = None

    def __post_init__(self):

        self._type = PropTypes.FILES


@dataclass
class FormulaFilter(PropFilter):
    """A filter for formula properties.

    Attributes:
        string: The result of formula is 'string' and property
            value matches the filter.
        checkbox: The result of the formula is 'checkbox' and
            property value matches the filter.
        number: The result of the formula is 'number' and property
            value matches the filter.
        date: The result of the formula is 'date' and property
            value matches the filter.
    """

    string: Optional[TextFilter] = None
    checkbox: Optional[CheckboxFilter] = None
    number: Optional[NumberFilter] = None
    date: Optional[DateFilter] = None

    def __post_init__(self):

        self._type = PropTypes.FORMULA

    def serialize(self) -> dict[str, Any]:

        filters: dict[str, Any] = {}
        attr_value: PropFilter
        for attr_name, attr_value in self.__dict__.items():

            if attr_value is not None and attr_name != "_type":
                filters[attr_name] = attr_value.serialize()

        return {self._type.value: filters}
