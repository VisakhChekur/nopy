from enum import Enum


class ObjectType(Enum):
    """The different types of objects in Notion."""

    DATABASE = "database"
    """A database object."""

    PAGE = "page"
    """A page object."""

    BLOCK = "block"
    """A block object."""

    COMMENT = "comment"
    """A comment object."""

    USER = "user"
    """A user object."""

    UNSUPPORTED = "unsupported"
    """An unsupported object."""
