from enum import Enum
from typing import Type

import nopy.props.db_props as dbp
from nopy.types import DBProps

API_VERSION = "2022-06-28"
API_BASE_URL = "https://api.notion.com/v1/"


class APIEndpoints(Enum):

    # Db related endpoints
    DB_CREATE = "databases"
    DB_RETRIEVE = "databases/{}"
    DB_QUERY = "databases/{}/query"
    DB_UPDATE = "databases/{}"

    # Page related endpoints
    PAGE_CREATE = "pages"
    PAGE_RETRIEVE = "pages/{}"
    PAGE_UPDATE = "pages/{}"

    # Block related endpoints
    BLOCK_CREATE = "blocks"
    BLOCK_RETRIEVE = "blocks/{}"
    BLOCK_UPDATE = "blocks/{}"
    BLOCK_CHILDREN_RETRIEVE = "blocks/{}/children"
    BLOCK_CHILDREN_APPEND = "blocks/{}"

    # Comment related endpoints
    COMMENT = "comment"

    # Users related endpoints
    USER_LIST = "users/"
    USER_RETRIEVE = "users/{}"
    USER_TOKEN_BOT = "users/me"

    # Search
    SEARCH = "search"


DB_PROPS_REVERSE_MAP: dict[str, Type[DBProps]] = {
    "checkbox": dbp.DBCheckbox,
    "created_by": dbp.DBCreatedBy,
    "created_time": dbp.DBCreatedTime,
    "date": dbp.DBDate,
    "email": dbp.DBEmail,
    "files": dbp.DBFiles,
    "formula": dbp.DBFormula,
    "last_edited_by": dbp.DBLastEditedBy,
    "last_edited_time": dbp.DBLastEditedTime,
    "multi_select": dbp.DBMultiSelect,
    "number": dbp.DBNumber,
    "people": dbp.DBPeople,
    "phone_number": dbp.DBPhoneNumber,
    "relation": dbp.DBRelation,
    "rollup": dbp.DBRollup,
    "rich_text": dbp.DBText,
    "select": dbp.DBSelect,
    "status": dbp.DBStatus,
    "url": dbp.DBUrl,
}
