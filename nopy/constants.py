from enum import Enum

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
