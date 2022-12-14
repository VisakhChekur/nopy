from dataclasses import dataclass
from typing import Any
from typing import Optional

from notion.query.filters import Filter
from notion.query.sorts import Sort


@dataclass
class Query:
    """A representation of a query to the Notion API."""

    and_filters: Optional[list[Filter]] = None
    or_filters: Optional[list[Filter]] = None
    sorts: Optional[list[Sort]] = None

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
