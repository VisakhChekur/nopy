from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Type

from nopy.objects.notion_object import NotionObject

@dataclass
class Comment(NotionObject):
    


    @classmethod
    def from_dict(cls: Type[Comment], args: dict[str, Any]) -> Comment:
        return Comment()