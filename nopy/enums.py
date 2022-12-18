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


class PropTypes(Enum):
    """The different types of properties."""

    UNSUPPORTED = "unsupported"
    """An unsupported property type."""

    CHECKBOX = "checkbox"
    """A checkbox property type."""

    CREATED_BY = "created_by"
    """A created by property type."""

    CREATED_TIME = "created_time"
    """A created time property type."""

    DATE = "date"
    """A date property type."""

    EMAIL = "email"
    """A email property type."""

    FILES = "files"
    """A files property type."""

    FORMULA = "formula"
    """A formula property type."""

    LAST_EDITED_BY = "last_edited_by"
    """A last edited by property type."""

    LAST_EDITED_TIME = "last_edited_time"
    """A last edited time property type."""

    MULTI_SELECT = "multi_select"
    """A multi select property type."""

    NUMBER = "number"
    """A number property type."""

    PEOPLE = "people"
    """A people property type."""

    PHONE_NUMBER = "phone_number"
    """A phone number property type."""

    RELATION = "relation"
    """A relation property type."""

    ROLLUP = "rollup"
    """A rollup property type."""

    RICH_TEXT = "rich_text"
    """A rich text property type."""

    SELECT = "select"
    """A select property type."""

    STATUS = "status"
    """A status property type."""

    TITLE = "title"
    """A title property type."""

    URL = "url"
    """A url property type."""


class Colors(Enum):
    """The possible colors."""

    DEFAULT = "default"
    """The default color."""

    GRAY = "gray"
    """A gray color."""

    BROWN = "brown"
    """A brown color."""

    ORANGE = "orange"
    """A orange color."""

    YELLOW = "yellow"
    """A yellow color."""

    GREEN = "green"
    """A green color."""

    BLUE = "blue"
    """A blue color."""

    PURPLE = "purple"
    """A purple color."""

    PINK = "pink"
    """A pink color."""

    RED = "red"
    """A red color."""

    GRAY_BACKGROUND = "gray_background"
    """A gray background color."""

    BROWN_BACKGROUND = "brown_background"
    """A brown background color."""

    ORANGE_BACKGROUND = "orange_background"
    """A orange background color."""

    YELLOW_BACKGROUND = "yellow_background"
    """A yellow background color."""

    GREEN_BACKGROUND = "green_background"
    """A green background color."""

    BLUE_BACKGROUND = "blue_background"
    """A blue background color."""

    PURPLE_BACKGROUND = "purple_background"
    """A purple background color."""

    PINK_BACKGROUND = "pink_background"
    """A pink background color."""

    RED_BACKGROUND = "red_background"
    """A red background color."""


class RichTextTypes(Enum):

    UNSUPPORTED = "unsupported"
    """An unsupported rich text type."""

    TEXT = "text"
    """A 'text' rich text."""

    MENTION = "mention"
    """A 'mention' rich text."""

    EQUATION = "equation"
    """An 'equation' rich text."""


class MentionTypes(Enum):
    """The mention types."""

    UNSUPPORTED = "unsupported"
    """An unsupported mention type."""

    USER = "user"
    """A user mention."""

    PAGE = "page"
    """A page mention."""

    DATABASE = "database"
    """A database mention."""

    DATE = "date"
    """A date mention."""

    LINK_PREVIEW = "link_preview"
    """A link preview mention."""


class UserType(Enum):

    UNSPPORTED = "unsupported"
    """An unsupported user type."""

    PERSON = "person"
    """A 'person' type user."""

    BOT = "bot"
    """A 'bot' type user."""


class FileTypes(Enum):
    """The file types."""

    FILE = "file"
    """A file hosted by Notion."""

    EXTERNAL = "external"
    """A file hosted externally, but rendered by Notion."""
