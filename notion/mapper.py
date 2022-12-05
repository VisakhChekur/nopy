from typing import TYPE_CHECKING
from typing import Any
from typing import Optional
from typing import Union

import dateutil.parser as date_parser

from notion.objects.db import Database
from notion.objects.properties import Properties
import notion.properties.common_properties as cp
import notion.properties.db_properties as dbp
from notion.typings import DBProps
from notion.typings import Parents

if TYPE_CHECKING:
    from notion.client import NotionClient

DB_PROPS_REVERSE_MAP: dict[str, type[DBProps]] = {
    "title": dbp.DBTitle,
    "rich_text": dbp.DBText,
    "number": dbp.DBNumber,
    "select": dbp.DBSelect,
    "multi_select": dbp.DBMultiSelect,
    "date": dbp.DBDate,
    "files": dbp.DBFiles,
    "checkbox": dbp.DBCheckbox,
    "url": dbp.DBUrl,
    "email": dbp.DBEmail,
    "phone_number": dbp.DBPhoneNumber,
    "formula": dbp.DBFormula,
    "created_time": dbp.DBCreatedTime,
    "created_by": dbp.DBCreatedBy,
    "last_edited_time": dbp.DBLastEditedTime,
    "last_edited_by": dbp.DBLastEditedBy,
    "status": dbp.DBStatus,
    "unsupported": dbp.DBProp,
}

PAGE_PROPS_REVERSE_MAP: dict[str, Any] = {}

PARENT_REVERSE_MAP: dict[str, type[Parents]] = {
    "database_id": cp.DatabaseParent,
    "page_id": cp.PageParent,
    "block_id": cp.BlockParent,
    "workspace": cp.WorkspaceParent,
}


class Mapper:
    """Handles mapping response from the Notion API to the correspoding 
    object."""

    # Also includes unsupported keys as well.
    UNNECESSARY_DB_KEYS = (
        "object",
        "created_by",
        "last_edited_by",
        "title",
        "description",
    )

    def __init__(self, client: Optional["NotionClient"] = None):

        self._client = client

    def map_to_db(self, db: dict[str, Any], *, no_mutate: bool = True) -> Database:

        if no_mutate:
            db = db.copy()

        db["cover"] = cp.File.from_dict(db["cover"])
        db["created_time"] = date_parser.parse(db["created_time"])
        db["last_edited_time"] = date_parser.parse(db["last_edited_time"])
        db["rich_title"] = [cp.Text.from_dict(t) for t in db["title"]]
        db["rich_description"] = [cp.Text.from_dict(t) for t in db["description"]]
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

    def _get_icon(self, icon_dict: dict[str, Any]) -> Union[cp.File, cp.Emoji]:
        """Gets the corresponding object of the Icon based on it's type."""

        if icon_dict["type"] == "emoji":
            return cp.Emoji.from_dict(icon_dict)
        return cp.File.from_dict(icon_dict)

    def _get_props(
        self, prop_dict: dict[str, Any], map: dict[str, type[DBProps]]
    ) -> Properties:
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
