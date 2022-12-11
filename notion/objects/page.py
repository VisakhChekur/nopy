from dataclasses import InitVar
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from typing import TYPE_CHECKING
from typing import Optional
from typing import Set
from typing import Union

import notion.properties.common_properties as cp
from notion.helpers import get_plain_text
from notion.objects.notion_object import NotionObject
from notion.objects.properties import Properties
from notion.typings import Parents

if TYPE_CHECKING:
    from notion.client import NotionClient


@dataclass
class Page(NotionObject):

    title: str = ""
    rich_title: list[cp.Text] = field(default_factory=list)
    properties: Properties = field(default_factory=Properties)
    created_time: Optional[datetime] = None
    last_edited_time: Optional[datetime] = None
    icon: Optional[Union[cp.File, cp.Emoji]] = None
    cover: Optional[cp.File] = None
    parent: Optional[Parents] = None
    url: str = ""
    archived: bool = False
    id: str = ""
    client: InitVar[Optional["NotionClient"]] = None

    def __post_init__(self, client: Optional["NotionClient"]):
        super().__post_init__(client)

        if self.rich_title:
            self.title = get_plain_text(self.rich_title)
        else:
            self.rich_title = [cp.Text(self.title)]

        self._og_props: Set[str] = set(self.properties.get_ids())

    def update(self):
        return super().update()

    def refresh(self, in_place: bool = True) -> "NotionObject":
        return super().refresh(in_place)
