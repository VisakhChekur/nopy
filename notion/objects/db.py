from dataclasses import InitVar
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from typing import TYPE_CHECKING
from typing import Any
from typing import Optional
from typing import Union

import notion.properties.common_properties as cp
from notion.helpers import get_plain_text
from notion.objects.notion_object import NotionObject
from notion.objects.properties import Properties
from notion.properties.base import BaseProperty
from notion.typings import Parents

if TYPE_CHECKING:
    from notion.client import NotionClient


@dataclass
class Database(NotionObject):
    """A representation of a Notion database.



    NOTE: rich_* has priority over their corresponding parts
    """

    title: str = ""
    rich_title: list[cp.Text] = field(default_factory=list)
    properties: Properties = field(default_factory=Properties)
    created_time: Optional[datetime] = None
    last_edited_time: Optional[datetime] = None
    description: str = ""
    rich_description: list[cp.Text] = field(default_factory=list)
    icon: Optional[Union[cp.File, cp.Emoji]] = None
    cover: Optional[cp.File] = None
    parent: Optional[Parents] = None
    url: str = ""
    archived: bool = False
    is_inline: bool = False
    id: str = ""
    client: InitVar[Optional["NotionClient"]] = None

    def __post_init__(self, client: Optional["NotionClient"]):
        super().__post_init__(client)

        if self.rich_title:
            self.title = get_plain_text(self.rich_title)
        else:
            self.rich_title.append(cp.Text(self.title))
        if self.rich_description:
            self.description = get_plain_text(self.rich_description)
        else:
            self.rich_description.append(cp.Text(self.title))
        # Keep track of the original properties if present so they can
        # be used later to determine whether to use the ID or the name
        # when serializing the properties.
        self._og_props = self.properties._ids  # type: ignore

    def refresh(self, in_place: bool = False):
        pass

    def update(self):
        # TODO: Checks to see if the required values are provided.
        pass

    def serialize_create(self) -> dict[str, Any]:

        serialized: dict[str, Any] = {
            "is_inline": self.is_inline,
            "properties": self._serialize_props(),
        }

        for key in ("parent", "icon", "cover"):
            attr: Optional[BaseProperty] = getattr(self, key)
            if attr:
                serialized[key] = attr.serialize_create()

        serialized["title"] = [t.serialize_create() for t in self.rich_title]
        serialized["description"] = [
            t.serialize_create() for t in self.rich_description
        ]

        return serialized

    def _serialize_props(self) -> dict[str, Any]:

        serialized_props: dict[str, Any] = {self.title: {"title": {}}}

        return serialized_props

    # If the id of the prop existed in the original props, use the id.
    # If not, use the name instead.
    # All properties to prioritize IDs over names where applicable.
