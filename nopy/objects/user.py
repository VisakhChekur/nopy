from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from typing import Type

from nopy.objects.notion_object import NotionObject


@dataclass
class User(NotionObject):
    @classmethod
    def from_dict(cls: Type[User], args: dict[str, Any]) -> User:
        return User()
