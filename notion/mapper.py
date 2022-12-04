from typing import TYPE_CHECKING
from typing import Any

from notion.objects.db import Database
from notion.properties.common_properties import Text
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
from notion.properties.properties import Properties
from notion.typings import DBProps

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
}


class Mapper:
    """Handles mapping response from the Notion API to the correspoding object."""

    def __init__(self, client: "NotionClient"):

        self._client = client

    def map_to_db(self, db_dict: dict[str, Any]) -> Database:

        # Mapping properties
        properties: Properties = Properties()
        for prop in db_dict["properties"].values():

            try:
                prop_cls = DB_PROPS_REVERSE_MAP[prop["type"]]
            except KeyError:
                # Means unsupported type
                prop_cls = DBProp
            properties._set_trusted(prop["id"], prop_cls(**prop))  # type: ignore
        db_dict["properties"] = properties

        # Getting title and description
        db_dict["db_title"] = [Text(**t) for t in db_dict["title"]]
        db_dict["db_description"] = [Text(**t) for t in db_dict["description"]]
        db_dict["_client"] = self._client
        return Database(**db_dict)
