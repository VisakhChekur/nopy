from dataclasses import InitVar
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from typing import TYPE_CHECKING
from typing import Any
from typing import ClassVar
from typing import Optional
from typing import Set
from typing import Union

import notion.properties.common_properties as cp
from notion.helpers import get_plain_text
from notion.objects.notion_object import NotionObject
from notion.objects.properties import Properties
from notion.properties.base import BaseProperty
from notion.properties.prop_enums import PropTypes
from notion.typings import Parents

if TYPE_CHECKING:
    from notion.client import NotionClient


@dataclass
class Database(NotionObject):
    """A representation of a Notion database.


    NOTE: rich_* has priority over their corresponding parts
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
        self._og_props: Set[str] = set(self.properties._ids.keys())  # type: ignore

    def set_client(self, client: "NotionClient"):
        self._client = client

    def refresh(self, in_place: bool = False) -> "Database":

        db = self._client.retrieve_db(self.id, use_cached=True)
        if in_place:
            self.__dict__.clear()
            self.__dict__ = db.__dict__
            return self
        return db

    def update(self):

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
