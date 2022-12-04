from dataclasses import InitVar
from datetime import datetime
from typing import TYPE_CHECKING, Optional, Union



from notion.objects.notion_object import NotionObject
from notion.properties.common import RichText, User, Emoji, File
from notion.properties.db_props import *
from notion.helpers import get_plain_text
from notion.typings import TEXT

if TYPE_CHECKING:
    from notion.client import NotionClient

# TODO: Add from_dict, from_json, from_pickle classmethods

@dataclass
class Database(NotionObject):
    """A representation of a Notion databse.
    
    Args:
        plain_title (str):
            The title of the database as plain text.
        title (list[RichText]):
            The list of `RichText` objects that describes how the title appears
            in Notion.
        properties (dict):
            A dictionary of
    """


    db_title: InitVar[TEXT]
    db_properties: InitVar[Optional[list[DBProp]]] = None
    _: dataclasses.KW_ONLY
    created_time: Optional[datetime] = None
    created_by: Optional[User] = None
    last_edited_time: Optional[datetime] = None
    last_edited_by: Optional[User] = None
    db_description: InitVar[Optional[TEXT]] = None
    icon: Optional[Union[File, Emoji]] = None
    cover: Optional[File] = None
    parent: Optional[dict[str, str]] = None
    url: Optional[str] = None
    archived: bool = False
    is_inline: bool = False
    client: InitVar[Optional["NotionClient"]] = None

    def __post_init__(self, db_title: TEXT, db_properties: Optional[list[DBProp]], db_description: Optional[TEXT], client: Optional["NotionClient"]):

        self._client = client

        # Converting list of properties to a dictionary
        if db_properties:
            self.properties = {}
        else:
            self.properties = {}

        # Setting up the database title
        if isinstance(db_title, str):
            self.plain_title = db_title
            self.title = [RichText(plain_text=db_title)]
        else:
            self.plain_title = get_plain_text(db_title)
            self.title = db_title

        # Setting up the database description
        if not db_description:
            return
        if isinstance(db_description, str):
            self.plain_description = db_description
            self.description = [RichText(plain_text=db_description)]
        else:
            self.plain_description = get_plain_text(db_description)
            self.description = db_description

    
    def serialize(self):
        
        import os
        serialized: dict[str, Any] = {
            "parent": {"type": "page_id", "page_id": os.environ["TEST_PAGE_ID"]},
        
            "title": [RichText(plain_text="Created Title").serialize()]
        }

        props = [DBText(name="some text"), DBNumber(name="some number", format=NumberFormats.RUPEE)]
        serialized["properties"] = {prop.name: prop.serialize() for prop in props}
        serialized["properties"]["title"] = {"title": {}}

        return serialized
    
    def update(self) -> None:
        pass

    def refresh(self) -> None:
        pass
