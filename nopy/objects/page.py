from dataclasses import InitVar
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from typing import TYPE_CHECKING
from typing import Optional
from typing import Set
from typing import Union

from ..helpers import get_plain_text
from ..properties import common_properties as cp
from ..typings import Parents
from .notion_object import NotionObject
from .properties import Properties

if TYPE_CHECKING:
    from nopy.client import NotionClient


@dataclass
class Page(NotionObject):
    """A representation of a Notion Page.

    Attributes:
        title: The title of the page without any annotations/styling.

        rich_title: The title of the page with the annotations/styling.

        properties: The properties of the page. Properties can be
                    accessed as a dictionary, but new properties can NOT
                    be added as possible within a dictionary.

        created_time: The time the page was created. Edits to this are
                      ignore during updating or creation of pages.

        last_edited_time: The time the page was last edited. Edits to
        this are ignore during updating or creation of pages.

        icon: The icon of the page, if any.

        cover: THe cover of the page, if any.

        parent: The parent of the page.

        url: The URL of the page.

        archived: Denotes whether the page is archived or not.

        id: The id of the page.


    """

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
