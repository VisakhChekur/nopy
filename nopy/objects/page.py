from __future__ import annotations

from dataclasses import InitVar
from dataclasses import dataclass
from dataclasses import field
from typing import TYPE_CHECKING
from typing import Any
from typing import ClassVar
from typing import Optional
from typing import Set
from typing import Type
from typing import Union
from typing import cast

from nopy.properties.page_properties import PTitle

from .. import mappers as mp
from ..helpers import TextDescriptor
from ..properties.common_properties import Emoji
from ..properties.common_properties import File
from ..properties.common_properties import Text
from ..reverse_maps import PAGE_PROPS_REVERSE_MAP
from .notion_object import NotionObject
from .properties import Properties

if TYPE_CHECKING:
    from nopy.client import NotionClient
    from nopy.objects.db import Database


@dataclass
class Page(NotionObject):
    """A representation of a Notion Page.

    Attributes:
        title (str): The title of the page without any annotations/styling.

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

    title: ClassVar[TextDescriptor] = TextDescriptor("rich_title")

    rich_title: list[Text] = field(default_factory=list)
    properties: Properties = field(default_factory=Properties)
    icon: Optional[Union[File, Emoji]] = None
    cover: Optional[File] = None
    url: str = ""
    client: InitVar[Optional["NotionClient"]] = None

    def __post_init__(self, client: Optional["NotionClient"]):
        super().__post_init__(client)

        self._og_props: Set[str] = set(self.properties._ids.keys())  # type: ignore

    def update(self):
        return super().update()

    def refresh(self, in_place: bool = True) -> "NotionObject":
        return super().refresh(in_place)

    @classmethod
    def from_dict(
        cls: Type[Page],
        page: dict[str, Any],
        client: "NotionClient",
        db: Optional[Database] = None,
    ) -> Page:

        properties = mp.get_props(page["properties"], PAGE_PROPS_REVERSE_MAP, db)
        # `title` is not directly provided as in the case of databases
        # which means it has to be found from the properties of the page
        title = cast(PTitle, properties["title"])

        page_args = {
            "properties": properties,
            "icon": mp.get_icon(page["icon"]),
            "cover": mp.get_cover(page["cover"]),
            "url": page["url"],
            "rich_title": title.rich_title,
        }
        page_args.update(mp.get_base_args(page, client))

        return Page(**page_args)
