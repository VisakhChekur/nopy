import dateutil.parser as date_parser
from copy import deepcopy
from typing import TYPE_CHECKING, Optional, Union
from typing import Any

from notion.objects.db import Database
from notion.properties.common_properties import BlockParent, DatabaseParent, Emoji, File, PageParent, Text, WorkspaceParent
from notion.properties.db_properties import DBCheckbox
from notion.properties.db_properties import DBCreatedBy
from notion.properties.db_properties import DBCreatedTime
from notion.properties.db_properties import DBDate
from notion.properties.db_properties import DBEmail
from notion.properties.db_properties import DBFiles
from notion.properties.db_properties import DBFormula
from notion.properties.db_properties import DBLastEditedBy
from notion.properties.db_properties import DBLastEditedTime
from notion.properties.db_properties import DBMultiSelect
from notion.properties.db_properties import DBNumber
from notion.properties.db_properties import DBPhoneNumber
from notion.properties.db_properties import DBProp
from notion.properties.db_properties import DBSelect
from notion.properties.db_properties import DBStatus
from notion.properties.db_properties import DBText
from notion.properties.db_properties import DBTitle
from notion.properties.db_properties import DBUrl
from notion.objects.properties import Properties
from notion.typings import DBProps, Parents

if TYPE_CHECKING:
    from notion.client import NotionClient

DB_PROPS_REVERSE_MAP: dict[str, type[DBProps]] = {
    "title": DBTitle,
    "rich_text": DBText,
    "number": DBNumber,
    "select": DBSelect,
    "multi_select": DBMultiSelect,
    "date": DBDate,
    "files": DBFiles,
    "checkbox": DBCheckbox,
    "url": DBUrl,
    "email": DBEmail,
    "phone_number": DBPhoneNumber,
    "formula": DBFormula,
    "created_time": DBCreatedTime,
    "created_by": DBCreatedBy,
    "last_edited_time": DBLastEditedTime,
    "last_edited_by": DBLastEditedBy,
    "status": DBStatus,
    "unsupported": DBProp
}

PAGE_PROPS_REVERSE_MAP: dict[str, Any] = {}

PARENT_REVERSE_MAP: dict[str, type[Parents]] = {
    "database_id": DatabaseParent,
    "page_id": PageParent,
    "block_id": BlockParent,
    "workspace": WorkspaceParent
}

class Mapper:
    """Handles mapping response from the Notion API to the correspoding object."""

    # Also includes unsupported keys as well.
    UNNECESSARY_DB_KEYS = ("object", "created_by", "last_edited_by", "title", "description")

    def __init__(self, client: Optional["NotionClient"]=None):

        self._client = client

    def map_to_db(self, db: dict[str, Any], *, no_mutate:bool=True) -> Database:

        if no_mutate:
            db = db.copy()
        
        db["cover"] = File.from_dict(db["cover"])
        db["created_time"] = date_parser.parse(db["created_time"])
        db["last_edited_time"] = date_parser.parse(db["last_edited_time"])
        db["rich_title"] = [Text.from_dict(t) for t in db["title"]]
        db["rich_description"] = [Text.from_dict(t) for t in db["description"]]
        db["icon"] = self._get_icon(db["icon"])
        db["properties"] = self._get_props(db["properties"], DB_PROPS_REVERSE_MAP)
        db["client"] = self._client
        
        # Getting parent
        parent_type = db["parent"]["type"]
        parent_class = PARENT_REVERSE_MAP[parent_type]
        db["parent"] = parent_class(db["parent"][parent_type])

        # Removing unsupported/unnecessary keys
        for key in Mapper.UNNECESSARY_DB_KEYS:
            db.pop(key)
        
        return Database(**db)
        
    def _get_icon(self, icon_dict: dict[str, Any]) -> Union[File, Emoji]:
        """Gets the corresponding object of the Icon based on it's type."""

        if icon_dict["type"] == "emoji":
            return Emoji.from_dict(icon_dict)
        return File.from_dict(icon_dict)
    
    def _get_props(self, prop_dict: dict[str, Any], map: dict[str, type[DBProps]]) -> Properties:
        # TODO: Change type hints once page and block properties are set as well
        
        props: Properties = Properties()
        for prop in prop_dict.values():
            try:
                prop_class = map[prop["type"]]
            except KeyError:
                prop_class = map["unsupported"]
            prop_instance = prop_class.from_dict(prop)

            props._set_trusted(prop_instance.id, prop_instance)  # type: ignore

        return props