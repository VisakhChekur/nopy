from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import TYPE_CHECKING
from typing import Any
from typing import ClassVar
from typing import Optional
from typing import Type
from typing import Union

from nopy.enums import ObjectTypes
from nopy.objects.notion_object import NotionObject
from nopy.props.common import Emoji
from nopy.props.common import File
from nopy.props.common import RichText
from nopy.utils import TextDescriptor
from nopy.utils import base_obj_args
from nopy.utils import get_cover
from nopy.utils import get_icon
from nopy.utils import rich_text_list

if TYPE_CHECKING:
    from nopy.client import NotionClient


@dataclass
class Page(NotionObject):
    """A representation of a page in Notion.

    Attributes:
        title (str): The title of the datbase without styling.

        rich_title: The title of the page with style information.

        icon: The icon of the page, if any.

        cover: The cover of the page, if any.

        url: The URL of the page, if any.

        archived (bool): Denotes whether the page is archived or not.

        id (str): The id of the page.

        parent (Parent): The parent of the page.

        created_time (Optional[datetime]):
            The time the page was created.

        last_edited_time (Optional[datetime]):
            The time the page was last edited.

        type (ObjectTypes):
            The type of the Notion object which will always be
            `ObjectTypes.PAGE`.

    """

    title: ClassVar[TextDescriptor] = TextDescriptor("rich_title")

    rich_title: list[RichText] = field(default_factory=list)
    icon: Optional[Union[File, Emoji]] = None
    cover: Optional[File] = None
    is_inline: bool = False
    url: str = ""

    def __post_init__(self, client: Optional["NotionClient"]):
        super().__post_init__(client)
        self._type = ObjectTypes.PAGE

    @classmethod
    def from_dict(cls: Type[Page], args: dict[str, Any]) -> Page:

        title_list = args["properties"]["title"]["title"]
        new_args: dict[str, Any] = {
            "rich_title": rich_text_list(title_list),
            "icon": get_icon(args["icon"]),
            "cover": get_cover(args["cover"]),
            "url": args["url"],
        }
        new_args.update(base_obj_args(args))

        return Page(**new_args)
