from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from typing import Type

from nopy.objects.notion_object import NotionObject


@dataclass
class Page(NotionObject):
    @classmethod
    def from_dict(cls: Type[Page], args: dict[str, Any]) -> Page:
        return Page()
