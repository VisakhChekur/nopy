from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Type

from nopy.objects.notion_object import NotionObject

@dataclass
class Database(NotionObject):
    


    @classmethod
    def from_dict(cls: Type[Database], args: dict[str, Any]) -> Database:
        return Database()