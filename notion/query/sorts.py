from dataclasses import dataclass
from typing import Literal
from typing import Union

from notion.properties.db_properties import DBProp

Direction = Literal["ascending", "descending"]


@dataclass
class PropertySort:

    property: Union[DBProp, str]
    direction: Direction

    def serialize(self) -> dict[str, str]:

        prop_name = (
            self.property if isinstance(self.property, str) else self.property.name
        )
        return {"property": prop_name, "direction": self.direction}


@dataclass
class TimestampSort:

    timestamp: Literal["created_time", "last_edited_time"]
    direction: Direction

    def serialize(self) -> dict[str, str]:

        return {"timestamp": self.timestamp, "direction": self.direction}


Sort = Union[PropertySort, TimestampSort]
