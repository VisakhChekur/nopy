from dataclasses import InitVar
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from typing import TYPE_CHECKING
from typing import Any
from typing import ClassVar
from typing import Generator
from typing import Optional
from typing import Set
from typing import Union

from ..helpers import TextDescriptor
from ..properties.base import BaseProperty
from ..properties.common_properties import Emoji
from ..properties.common_properties import File
from ..properties.common_properties import Text
from ..properties.prop_enums import PropTypes
from ..query.query import Query
from ..typings import Parents
from .notion_object import NotionObject
from .properties import Properties

if TYPE_CHECKING:
    from nopy.client import NotionClient
    from nopy.objects.page import Page


@dataclass
class Database(NotionObject):
    """A representation of a Notion database.

    Attributes:
        title: The title of the database without any annotations/styling.

        rich_title: The title of the database with the annotations/styling.

        properties: The properties of the database. Properties can be
                    accessed as a dictionary, but new properties can NOT
                    be added as possible within a dictionary.

        created_time: The time the database was created. Edits to this are
                      ignore during updating or creation of databases.

        last_edited_time: The time the database was last edited. Edits to
        this are ignore during updating or creation of databases.

        description: The description of the database in Notion without the
                     annotations/styling.

        rich_description: The description of the database in Notion with the
                          annotations/styling.

        icon: The icon of the database, if any.

        cover: THe cover of the database, if any.

        parent: The parent of the database.

        url: The URL of the database.

        archived: Denotes whether the database is archived or not.

        is_inline: Denotes whether the database is inlined within a page
                   or not.

        id: The id of the database.

    NOTE: rich_* has priority over their corresponding parts during creation
    and updation of databases.
    """

    # Properties to skip in serialization since they can't be updated
    # nor created by the user. TITLE is an exception since it's a MUST
    # in every request, that will be handled by the serialization logic
    # separately to ensure it's present.
    _SKIP_SERIALIZE: ClassVar[Set[PropTypes]] = {
        PropTypes.CREATED_BY,
        PropTypes.CREATED_TIME,
        PropTypes.LAST_EDITED_BY,
        PropTypes.LAST_EDITED_TIME,
        PropTypes.TITLE,
    }
    title: ClassVar[TextDescriptor] = TextDescriptor("rich_title")
    description: ClassVar[TextDescriptor] = TextDescriptor("rich_description")

    rich_title: list[Text] = field(default_factory=list)
    properties: Properties = field(default_factory=Properties)
    created_time: Optional[datetime] = None
    last_edited_time: Optional[datetime] = None
    rich_description: list[Text] = field(default_factory=list)
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

        # Keep track of the original properties if present so they can
        # be used later to determine whether to use the ID or the name
        # when serializing the properties.
        self._og_props: Set[str] = set(self.properties._ids.keys())  # type: ignore

    def query(self, query: Optional[Query] = None) -> Generator["Page", None, None]:
        """Returns a generator that yields a single page at a time that
        satisfies the query conditions.

        Args:
            query: The query to perform on the database. If it is `None`, then
                   it is the same as `get_pages()` method on this class.

        Returns:
            A generator that yields a single page at a time.

        Raises:
            ValueError: `NotionClient` instance was not provided either during
                        the creation of the instance or via the `set_client()`
                        method.
        """
        if not self._client:
            raise ValueError("'client' must be provided")

        if not query:
            return self.get_pages()

        return self._query(query.serialize())

    def get_pages(self, page_size: int = 100) -> Generator["Page", None, None]:
        """Returns a generator that yields a single page at a time.

        Args:
            page_size: The number of pages that's received from each API call.

        Returns:
            A generator that yields a single page at a time.

        Raises:
            ValueError: `NotionClient` instance was not provided either during
                        the creation of the instance or via the `set_client()`
                        method.
        """

        if not self._client:
            raise ValueError("'client' must be provided")

        query = {"page_size": page_size}
        return self._query(query)

    def set_client(self, client: "NotionClient"):
        """Set the client."""

        self._client = client

    def refresh(self, in_place: bool = False) -> "Database":
        """Refreshes the database.

        Makes a new call to the Notion API and gets the latest version of
        the database avaiable with Notion.

        Args:
            in_place: If `True`, a new instance of the database is returned
                      and the current instance is NOT modified.

        Returns:
            The "refreshed" database.

        Raises:
            ValueError: `NotionClient` instance was not provided either during
                        the creation of the instance or via the `set_client()`
                        method. Also raised, if the `id` of the database is not
                        provided.
        """

        if not self._client:
            raise ValueError("'client' must be provided")
        if not self.id:
            raise ValueError("'id' must be provided")

        db = self._client.retrieve_db(self.id, use_cached=False)
        if in_place:
            self.__dict__.clear()
            self.__dict__ = db.__dict__
            return self
        return db

    def update(self) -> None:
        """Updates the current version of the database to Notion.

        Raises:
            ValueError: `NotionClient` instance was not provided either during
                        the creation of the instance or via the `set_client()`
                        method. Also raised, if the `id` of the database is not
                        provided.
        """
        if not self.id:
            raise ValueError("'id' must be provided")
        if not self._client:
            raise ValueError("'client' must be provided")

        serialized = self.serialize()
        deleted_props = self._serialize_deleted_props()
        serialized["properties"].update(deleted_props)
        # 'parent' is not allowed when updating databases
        serialized.pop("parent")
        self._client.update_db(self.id, serialized)
        self._og_props = set(self.properties.get_ids())

    def serialize(self) -> dict[str, Any]:
        """Serializes the instance to a format that adheres to the Notion
        specifications when creating/updating a database."""

        serialized: dict[str, Any] = {
            "is_inline": self.is_inline,
            "archived": self.archived,
            "properties": self._serialize_props(),
        }

        for key in ("parent", "icon", "cover"):
            attr: Optional[BaseProperty] = getattr(self, key)
            if attr:
                serialized[key] = attr.serialize()

        serialized["title"] = [t.serialize() for t in self.rich_title]
        serialized["description"] = [t.serialize() for t in self.rich_description]

        return serialized

    def _serialize_props(self) -> dict[str, Any]:

        serialized_props: dict[str, Any] = {self.title: {"title": {}}}

        for name, prop in self.properties.iter_names():
            if prop.type in Database._SKIP_SERIALIZE:
                continue
            if prop.id:
                serialized_props[prop.name] = prop.serialize()
            else:
                serialized_props[name] = prop.serialize()

        return serialized_props

    def _serialize_deleted_props(self) -> dict[str, None]:

        # Finding the properties that were deleted so that their values
        # can be correspondingly set
        curr_prop_ids = set(self.properties.get_ids())
        deleted_prop_ids = self._og_props.difference(curr_prop_ids)
        return {prop_id: None for prop_id in deleted_prop_ids}

    def _query(self, query_dict: dict[str, Any]) -> Generator["Page", None, None]:

        while True:
            query_results = self._client.query_db_raw(self.id, query_dict)
            for page in query_results["results"]:
                yield self._client._mapper.map_to_page(page, self)  # type: ignore
            if not query_results["has_more"]:
                break
            query_dict["start_cursor"] = query_results["next_cursor"]
