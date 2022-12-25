from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Union

from nopy.filters import Filter
from nopy.sorts import PropertySort
from nopy.sorts import TimestampSort


@dataclass
class Query:
    """A representation of a query to the Notion API.

    Attributes:
        and_filters: The filters which are chained by "and".
        or_filters: The filters which are chained by "or".
        sorts: The sorts to be applied to the results.
    """

    and_filters: list[Filter] = field(default_factory=list)
    or_filters: list[Filter] = field(default_factory=list)
    sorts: list[Union[TimestampSort, PropertySort]] = field(default_factory=list)

    def serialize(self):

        serialized: dict[str, Any] = {"filter": {}}

        if self.and_filters:
            serialized["filter"]["and"] = [
                filter.serialize() for filter in self.and_filters
            ]
        if self.or_filters:
            serialized["filter"]["or"] = [
                filter.serialize() for filter in self.or_filters
            ]
        if self.sorts:
            serialized["sorts"] = [sort.serialize() for sort in self.sorts]

        return serialized
