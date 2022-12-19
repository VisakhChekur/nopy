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
class Database(NotionObject):
    """A representation of a database in Notion.

    Attributes:
        title (str): The title of the datbase without styling.

        rich_title: The title of the database with style information.

        description (str): The description of the database without styling.

        rich_description:
            The description of the database with sytle information.

        icon: The icon of the database, if any.

        cover: The cover of the database, if any.

        is_inline: Denotes whether the database is inline or not.

        url: The URL of the database, if any.

        archived (bool): Denotes whether the database is archived or not.

        id (str): The id of the database.

        parent (Parent): The parent of the database.

        created_time (Optional[datetime]):
            The time the database was created.

        last_edited_time (Optional[datetime]):
            The time the database was last edited.

        type (ObjectTypes):
            The type of the Notion object which will always be
            `ObjectTypes.DATABASE`.

    """

    title: ClassVar[TextDescriptor] = TextDescriptor("rich_title")
    description: ClassVar[TextDescriptor] = TextDescriptor("rich_description")

    rich_title: list[RichText] = field(default_factory=list)
    rich_description: list[RichText] = field(default_factory=list)
    icon: Optional[Union[File, Emoji]] = None
    cover: Optional[File] = None
    is_inline: bool = False
    url: str = ""

    def __post_init__(self, client: Optional["NotionClient"]):
        super().__post_init__(client)
        self._type = ObjectTypes.DATABASE

    @classmethod
    def from_dict(cls: Type[Database], args: dict[str, Any]) -> Database:

        new_args: dict[str, Any] = {
            "rich_title": rich_text_list(args["title"]),
            "rich_description": rich_text_list(args["description"]),
            "icon": get_icon(args["icon"]),
            "cover": get_cover(args["cover"]),
            "is_inline": args["is_inline"],
            "url": args["url"],
        }
        new_args.update(base_obj_args(args))

        return Database(**new_args)
