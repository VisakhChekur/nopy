from enum import Enum


class PropTypes(Enum):
    """The different property types available on databases/pages.

    Args:
        TITLE: A title property.
        RICH_TEXT: A rich text property.
        NUMBER: A number property.
        SELECT: A select property.
        MULTI_SELECT: A multi select property.
        DATE: A date property.
        FILES: A files property.
        CHECKBOX: A checkbox property.
        URL: A url property.
        EMAIL: An email property.
        PHONE_NUMBER: A phone number property.
        FORMULA: A formula property.
        CREATED_TIME: A created time property.
        CREATED_BY: A created by property.
        LAST_EDITED_TIME: A last edited time property.
        LAST_EDITED_BY: A last edited by property.
        STATUS: A status property.
        UNSUPPORTED: An unsupported property.
    """

    TITLE = "title"
    RICH_TEXT = "rich_text"
    NUMBER = "number"
    SELECT = "select"
    MULTI_SELECT = "multi_select"
    DATE = "date"
    # PEOPLE = "people"
    FILES = "files"
    CHECKBOX = "checkbox"
    URL = "url"
    EMAIL = "email"
    PHONE_NUMBER = "phone_number"
    FORMULA = "formula"
    # RELATION = "relation"
    # ROLLUP = "rollup"
    CREATED_TIME = "created_time"
    CREATED_BY = "created_by"
    LAST_EDITED_TIME = "last_edited_time"
    LAST_EDITED_BY = "last_edited_by"
    STATUS = "status"
    UNSUPPORTED = "unsupported"


class NumberFormat(Enum):
    """The different types of number formats possible.

    Args:
        NUMBER: A number format.
        NUMBER_WITH_COMMAS: A number with commas format.
        PERCENT: A percent format.
        DOLLAR: A dollar format.
        CANADIAN_DOLLAR: A canadian dollar format.
        EURO: A euro format.
        POUND: A pound format.
        YEN: A yen format.
        RUBLE: A ruble format.
        RUPEE: A rupee format.
        WON: A won format.
        YUAN: A yuan format.
        REAL: A real format.
        LIRA: A lira format.
        RUPIAH: A rupiah format.
        FRANC: A franc format.
        HONG_KONG_DOLLAR: A hong kong dollar format.
        NEW_ZEALAND_DOLLAR: A new zealand dollar format.
        KRONA: A krona format.
        NORWEGIAN_KRONE: A norwegian krone format.
        MEXICAN_PESO: A mexican peso format.
        RAND: A rand format.
        NEW_TAIWAN_DOLLAR: A new taiwan dollar format.
        DANISH_KRONE: A danish krone format.
        ZLOTY: A zloty format.
        BAHT: A baht format.
        FORINT: A forint format.
        KORUNA: A koruna format.
        SHEKEL: A shekel format.
        CHILEAN_PESO: A chilean peso format.
        PHILIPPINE_PESO: A philippine peso format.
        DIRHAM: A dirham format.
        COLOMBIAN_PESO: A colombian peso format.
        RIYAL: A riyal format.
        RINGGIT: A ringgit format.
        LEU: A leu format.
        ARGENTINE_PESO: A argentine peso format.
        URUGUAYAN_PESO: A uruguayan peso format.
        SINGAPORE_DOLLAR: A singapore dollar format.
    """

    NUMBER = "number"
    NUMBER_WITH_COMMAS = "number_with_commas"
    PERCENT = "percent"
    DOLLAR = "dollar"
    CANADIAN_DOLLAR = "canadian_dollar"
    EURO = "euro"
    POUND = "pound"
    YEN = "yen"
    RUBLE = "ruble"
    RUPEE = "rupee"
    WON = "won"
    YUAN = "yuan"
    REAL = "real"
    LIRA = "lira"
    RUPIAH = "rupiah"
    FRANC = "franc"
    HONG_KONG_DOLLAR = "hong_kong_dollar"
    NEW_ZEALAND_DOLLAR = "new_zealand_dollar"
    KRONA = "krona"
    NORWEGIAN_KRONE = "norwegian_krone"
    MEXICAN_PESO = "mexican_peso"
    RAND = "rand"
    NEW_TAIWAN_DOLLAR = "new_taiwan_dollar"
    DANISH_KRONE = "danish_krone"
    ZLOTY = "zloty"
    BAHT = "baht"
    FORINT = "forint"
    KORUNA = "koruna"
    SHEKEL = "shekel"
    CHILEAN_PESO = "chilean_peso"
    PHILIPPINE_PESO = "philippine_peso"
    DIRHAM = "dirham"
    COLOMBIAN_PESO = "colombian_peso"
    RIYAL = "riyal"
    RINGGIT = "ringgit"
    LEU = "leu"
    ARGENTINE_PESO = "argentine_peso"
    URUGUAYAN_PESO = "uruguayan_peso"
    SINGAPORE_DOLLAR = "singapore_dollar"


class Colors(Enum):
    """The different types of supported colors.

    Args:
        DEFAULT: Default color.
        GRAY: Gray color.
        BROWN: Brown color.
        ORANGE: Orange color.
        YELLOW: Yellow color.
        GREEN: Green color.
        BLUE: Blue color.
        PURPLE: Purple color.
        PINK: Pink color.
        RED: Red color.
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


class RichTextTypes(Enum):
    """The supported rich text types.

    NOTE: Not all rich text types supported by the official Notion API
    is supported by the library currently.

    Args:
        TEXT: A text type rich text.
        UNUSPPORTED: An unuspported type.
    """

    TEXT = "text"
    UNSUPPORTED = "unsupported"


class FileTypes(Enum):
    """The file types.

    Args:
        FILE: A file hosted by Notion.
        EXTERNAL: A file hosted externally, but rendered by Notion.
    """

    FILE = "file"
    EXTERNAL = "external"


class EmojiTypes(Enum):
    """The types of Emojis.

    Args:
        EMOJI: The Emoji type.
    """

    EMOJI = "emoji"


class ParentTypes(Enum):
    """The formula types.

    Args:
        DATABASE: A Database parent.
        PAGE: A Page parent.
        WORKSPACE: A Workspace parent.
        BLOCK: A Block parent.
        UNSUPPORTED: An Unsupported parent.
    """

    DATABASE = "database_id"
    PAGE = "page_id"
    WORKSPACE = "workspace"
    BLOCK = "block_id"
    UNSUPPORTED = "unsupported"


class FormulaTypes(Enum):
    """The formula types.

    Args:
        NUMBER: A number formula.
        STRING: A string formula.
        BOOLEAN: A boolean formula.
        DATE: A date formula.
    """

    NUMBER = "number"
    STRING = "string"
    BOOLEAN = "boolean"
    DATE = "date"

    # """The parent types.

    # Args:
    # """
