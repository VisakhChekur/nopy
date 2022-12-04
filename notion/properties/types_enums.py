
from enum import Enum

class PropTypes(Enum):
    """Enums for the property types of pages and databases."""

    TITLE = "title"
    RICH_TEXT = "rich_text"
    NUMBER = "number"
    SELECT = "select"
    MULTI_SELECT = "multi_select"
    DATE = "date"
    PEOPLE = "people"
    FILES = "files"
    CHECKBOX = "checkbox"
    URL = "url"
    EMAIL = "email"
    PHONE_NUMBER = "phone_number"
    CREATED_TIME = "created_time"
    CREATED_BY = "created_by"
    LAST_EDITED_TIME = "last_edited_time"
    LAST_EDITED_BY = "last_edited_by"
    STATUS = "status"
    FORMULA = "formula"
    UNSUPPORTED = "unsupported"

PROP_TYPES_REVERSE_MAP = {prop.value: prop for prop in PropTypes}

class RichTextTypes(Enum):
    """Enums for the rich text types."""

    TEXT = "text"
    UNSUPPORTED = "unsupported"

RICH_TEXT_TYPES_REVERSE_MAP = {prop.value: prop for prop in RichTextTypes}

class NumberFormats(Enum):
    """Enums for the number format."""
    
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

NUMBER_FORMAT_REVERSE_MAP = {prop.value: prop for prop in NumberFormats}

class Colors(Enum):

    DEFAULT = "default"
    GRAY = "gray"
    GREY = "gray"
    BROWN = "brown"
    ORANGE = "orange"
    YELLOW = "yellow"
    GREEN = "green"
    BLUE = "blue"
    PURPLE = "purple"
    PINK = "pink"
    RED = "red"

COLORS_REVERSE_MAP = {prop.value: prop for prop in Colors}

class FileTypes(Enum):

    EXTERNAL = "external"
    FILE = "file"

FILE_TYPES_REVERSE_MAP = {prop.value: prop for prop in FileTypes}

class EmojiTypes(Enum):

    EMOJI = "emoji"