from enum import Enum


class Colors(Enum):
    """The different colors.

    Attributes:

        DEFAULT: The default color.
        GRAY: A gray color.
        BROWN: A brown color.
        ORANGE: A orange color.
        YELLOW: A yellow color.
        GREEN: A green color.
        BLUE: A blue color.
        PURPLE: A purple color.
        PINK: A pink color.
        RED: A red color.
        GRAY_BACKGROUND: A gray background color.
        BROWN_BACKGROUND: A brown background color.
        ORANGE_BACKGROUND: A orange background color.
        YELLOW_BACKGROUND: A yellow background color.
        GREEN_BACKGROUND: A green background color.
        BLUE_BACKGROUND: A blue background color.
        PURPLE_BACKGROUND: A purple background color.
        PINK_BACKGROUND: A pink background color.
        RED_BACKGROUND: A red background color.
    """

    DEFAULT = "default"
    GRAY = "gray"
    BROWN = "brown"
    ORANGE = "orange"
    YELLOW = "yellow"
    GREEN = "green"
    BLUE = "blue"
    PURPLE = "purple"
    PINK = "pink"
    RED = "red"
    GRAY_BACKGROUND = "gray_background"
    BROWN_BACKGROUND = "brown_background"
    ORANGE_BACKGROUND = "orange_background"
    YELLOW_BACKGROUND = "yellow_background"
    GREEN_BACKGROUND = "green_background"
    BLUE_BACKGROUND = "blue_background"
    PURPLE_BACKGROUND = "purple_background"
    PINK_BACKGROUND = "pink_background"
    RED_BACKGROUND = "red_background"


class FileTypes(Enum):
    """The different file types.

    Attributes:

        FILE: A file hosted by Notion.
        EXTERNAL: A file hosted externally, but rendered by Notion.
    """

    FILE = "file"
    EXTERNAL = "external"


class MentionTypes(Enum):
    """The different mention types.

    Attributes:

        UNSUPPORTED: An unsupported mention type.
        USER: A user mention.
        PAGE: A page mention.
        DATABASE: A database mention.
        DATE: A date mention.
        LINK_PREVIEW: A link preview mention.
    """

    UNSUPPORTED = "unsupported"
    USER = "user"
    PAGE = "page"
    DATABASE = "database"
    DATE = "date"
    LINK_PREVIEW = "link_preview"


class ObjectTypes(Enum):
    """The different object types.

    Attributes:

        DATABASE: A database object.
        PAGE: A page object.
        BLOCK: A block object.
        COMMENT: A comment object.
        USER: A user object.
        UNSUPPORTED: An unsupported object.
    """

    DATABASE = "database"
    PAGE = "page"
    BLOCK = "block"
    COMMENT = "comment"
    USER = "user"
    UNSUPPORTED = "unsupported"


class PropTypes(Enum):
    """The different prop types.

    Attributes:

        UNSUPPORTED: An unsupported property type.
        CHECKBOX: A checkbox property type.
        CREATED_BY: A created by property type.
        CREATED_TIME: A created time property type.
        DATE: A date property type.
        EMAIL: A email property type.
        FILES: A files property type.
        FORMULA: A formula property type.
        LAST_EDITED_BY: A last edited by property type.
        LAST_EDITED_TIME: A last edited time property type.
        MULTI_SELECT: A multi select property type.
        NUMBER: A number property type.
        PEOPLE: A people property type.
        PHONE_NUMBER: A phone number property type.
        RELATION: A relation property type.
        ROLLUP: A rollup property type.
        RICH_TEXT: A rich text property type.
        SELECT: A select property type.
        STATUS: A status property type.
        TITLE: A title property type.
        URL: A url property type.
    """

    UNSUPPORTED = "unsupported"
    CHECKBOX = "checkbox"
    CREATED_BY = "created_by"
    CREATED_TIME = "created_time"
    DATE = "date"
    EMAIL = "email"
    FILES = "files"
    FORMULA = "formula"
    LAST_EDITED_BY = "last_edited_by"
    LAST_EDITED_TIME = "last_edited_time"
    MULTI_SELECT = "multi_select"
    NUMBER = "number"
    PEOPLE = "people"
    PHONE_NUMBER = "phone_number"
    RELATION = "relation"
    ROLLUP = "rollup"
    RICH_TEXT = "rich_text"
    SELECT = "select"
    STATUS = "status"
    TITLE = "title"
    URL = "url"


class RichTextTypes(Enum):
    """The different rich text types.

    Attributes:

        UNSUPPORTED: An unsupported rich text type.
        TEXT: A 'text' rich text.
        MENTION: A 'mention' rich text.
        EQUATION: An 'equation' rich text.
    """

    UNSUPPORTED = "unsupported"
    TEXT = "text"
    MENTION = "mention"
    EQUATION = "equation"


class UserTypes(Enum):
    """The different user types.

    Attributes:

        UNSPPORTED: An unsupported user type.
        PERSON: A 'person' type user.
        BOT: A 'bot' type user.
    """

    UNSPPORTED = "unsupported"
    PERSON = "person"
    BOT = "bot"
