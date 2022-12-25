from dataclasses import dataclass
from typing import Literal
from typing import Union

from nopy.types import DBProps


@dataclass
class PropertySort:
    """A property based sort.

    Attributes:
        prop (Union[DBProps, str]): The property or the property id to
            sort with.
        direction: The direction to sort in.
    """

    property: Union[DBProps, str]
    direction: Literal["ascending", "descending"] = "ascending"

    def serialize(self) -> dict[str, str]:

        prop_name = (
            self.property if isinstance(self.property, str) else self.property.name
        )
        return {"property": prop_name, "direction": self.direction}


@dataclass
class TimestampSort:
    """A timestamp based sort.

    Attributes:
        timestamp: The timestamp to sort by.
        direction: The direction to sort in.
    """

    timestamp: Literal["created_time", "last_edited_time"]
    direction: Literal["ascending", "descending"] = "ascending"

    def serialize(self) -> dict[str, str]:

        return {"timestamp": self.timestamp, "direction": self.direction}
