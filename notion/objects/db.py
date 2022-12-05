from dataclasses import InitVar
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from typing import TYPE_CHECKING
from typing import Any
from typing import Iterable
from typing import Optional
from typing import Union

from notion.helpers import get_plain_text
from notion.objects.notion_object import NotionObject
from notion.objects.properties import Properties
from notion.properties.common_properties import Emoji
from notion.properties.common_properties import File
from notion.properties.common_properties import Text
from notion.typings import Parents

if TYPE_CHECKING:
    from notion.client import NotionClient


@dataclass
class Database(NotionObject):
    """A representation of a Notion database.

    NOTE: rich_* has priority over their corresponding parts
    """

    title: str = ""
    rich_title: Iterable[Text] = field(default_factory=list)
    properties: Properties = field(default_factory=Properties)
    created_time: Optional[datetime] = None
    last_edited_time: Optional[datetime] = None
    description: str = ""
    rich_description: Iterable[Text] = field(default_factory=list)
    icon: Optional[Union[File, Emoji]] = None
    cover: Optional[File] = None
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
        if self.rich_description:
            self.description = get_plain_text(self.rich_description)
        # Keep track of the original properties if present so they can
        # be used later to determine whether to use the ID or the name
        # when serializing the properties.
        self._og_props = self.properties._ids  # type: ignore

    def refresh(self, in_place: bool = False):
        pass

    def update(self):
        pass

    def serialize(self) -> dict[str, Any]:
        return {}
