from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import TYPE_CHECKING
from typing import Any
from typing import ClassVar
from typing import Generator
from typing import Optional
from typing import Set
from typing import Type
from typing import Union

from nopy.enums import ObjectTypes
from nopy.errors import NoClientFoundError
from nopy.objects.notion_object import NotionObject
from nopy.objects.page import Page
from nopy.properties import Properties
from nopy.props.common import Emoji
from nopy.props.common import File
from nopy.props.common import RichText
from nopy.utils import TextDescriptor
from nopy.utils import base_obj_args
from nopy.utils import get_cover
from nopy.utils import get_icon
from nopy.utils import get_props
from nopy.utils import paginate
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

        properties: The properties of the database.

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

    properties: Properties = field(default_factory=Properties)
    rich_title: list[RichText] = field(default_factory=list)
    rich_description: list[RichText] = field(default_factory=list)
    icon: Optional[Union[File, Emoji]] = None
    cover: Optional[File] = None
    is_inline: bool = False
    url: str = ""

    def __post_init__(self, client: Optional["NotionClient"]):
        super().__post_init__(client)

        self._type = ObjectTypes.DATABASE
        # Storing the ids of the original properties to handle
        # deleted properties.
        self._og_props = set(self.properties._ids.keys())  # type: ignore

    def get_pages(
        self, max_pages: int = 0, page_size: int = 100
    ) -> Generator[Page, None, None]:
        """Returns a generator that yields a single page at a time.

        Args:
            max_pages: The maximum number of pages to return.
            page_size:
                The number of pages to get from the Notion API per
                API call.

        Returns:
            A generator that yields a single page at a time.
        """
        if not self._client:
            raise NoClientFoundError("database")

        return paginate(
            self._client._query_db,  # type: ignore
            Page.from_dict,
            page_size=page_size,
            max_pages=max_pages,
            db_id=self.id,
            client=self._client,
        )

    def update(self, in_place: bool = False) -> Database:
        """Updates the database.

        Attributes:
            in_place:
                If `True`, then this instance is updated in place.

        Returns:
            The updated Database instance. Returns `self` if `in_place` is
            `True`.
        """

        if not self._client:
            raise NoClientFoundError("no client is associated with this instance")

        db = self.serialize()
        # Parent should not be present when updating
        db.pop("parent")

        updated_db = self._client.update_db(self.id, db)
        # Deleted properties have to be sent as a different update
        # request. Sending the deleted properties in one request does NOT
        # work.
        deleted_props = self._find_deleted_props()
        if deleted_props:
            db["properties"] = {prop_id: None for prop_id in deleted_props}
            updated_db = self._client.update_db(self.id, db)

        if not in_place:
            return updated_db
        self.__dict__.clear()
        self.__dict__ = updated_db.__dict__
        return self

    def serialize(self) -> dict[str, Any]:

        serialized: dict[str, Any] = {
            "is_inline": self.is_inline,
            "archived": self.archived,
            "properties": self.properties.serialize(),
        }

        # Serialize only if they're not None
        for attr in ("parent", "icon", "cover"):
            value = self.__dict__.get(attr, None)
            serialized[attr] = value if value is None else value.serialize()

        serialized["title"] = [rt.serialize() for rt in self.rich_title]
        serialized["description"] = [rt.serialize() for rt in self.rich_description]

        # Title needs to be added to the properties as well
        serialized["properties"]["title"] = {"title": {}}

        return serialized

    def _find_deleted_props(self) -> Set[str]:

        curr_props = set(self.properties._ids.keys())  # type: ignore
        return self._og_props.difference(curr_props)

    @classmethod
    def from_dict(cls: Type[Database], args: dict[str, Any]) -> Database:

        new_args: dict[str, Any] = {
            "rich_title": rich_text_list(args["title"]),
            "rich_description": rich_text_list(args["description"]),
            "icon": get_icon(args["icon"]),
            "cover": get_cover(args["cover"]),
            "is_inline": args["is_inline"],
            "url": args["url"],
            "properties": get_props(args["properties"]),
        }
        new_args.update(base_obj_args(args))

        return Database(**new_args)
