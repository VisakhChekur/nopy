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


class ParentTypes(Enum):
    """The different parent types.

    Attributes:
        DATABASE (ParentTypes): A database parent.
        PAGE (ParentTypes): A page parent.
        BLOCK (ParentTypes): A block parent.
        WORKSPACE (ParentTypes): A workspace parent.
        UNSUPPORTED (ParentTypes): An unsupported parent.
    """

    DATABASE = "database_id"
    PAGE = "page_id"
    BLOCK = "block_id"
    WORKSPACE = "workspace"
    UNSUPPORTED = "unsupported"


class NumberFormat(Enum):
    """The different types of number formats possible.

    Attributes:
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


class RollupFunctions(Enum):
    """All the rollup functions.

    Attributes:
        COUNT: A 'count' function.
        COUNT_VALUES: A 'count values' function.
        EMPTY: A 'empty' function.
        NOT_EMPTY: A 'not empty' function.
        UNIQUE: A 'unique' function.
        SHOW_UNIQUE: A 'show unique' function.
        PERCENT_EMPTY: A 'percent empty' function.
        PERCENT_NOT_EMPTY: A 'percent not empty' function.
        SUM: A 'sum' function.
        AVERAGE: A 'average' function.
        MEDIAN: A 'median' function.
        MIN: A 'min' function.
        MAX: A 'max' function.
        RANGE: A 'range' function.
        EARLIEST_DATE: A 'earliest date' function.
        LATEST_DATE: A 'latest date' function.
        DATE_RANGE: A 'date range' function.
        CHECKED: A 'checked' function.
        UNCHECKED: A 'unchecked' function.
        PERCENT_CHECKED: A 'percent checked' function.
        PERCENT_UNCHECKED: A 'percent unchecked' function.
        COUNT_PER_GROUP: A 'count per group' function.
        PERCENT_PER_GROUP: A 'percent per group' function.
        SHOW_ORIGINAL: A 'show original' function.
    """

    COUNT = "count"
    COUNT_VALUES = "count_values"
    EMPTY = "empty"
    NOT_EMPTY = "not_empty"
    UNIQUE = "unique"
    SHOW_UNIQUE = "show_unique"
    PERCENT_EMPTY = "percent_empty"
    PERCENT_NOT_EMPTY = "percent_not_empty"
    SUM = "sum"
    AVERAGE = "average"
    MEDIAN = "median"
    MIN = "min"
    MAX = "max"
    RANGE = "range"
    EARLIEST_DATE = "earliest_date"
    LATEST_DATE = "latest_date"
    DATE_RANGE = "date_range"
    CHECKED = "checked"
    UNCHECKED = "unchecked"
    PERCENT_CHECKED = "percent_checked"
    PERCENT_UNCHECKED = "percent_unchecked"
    COUNT_PER_GROUP = "count_per_group"
    PERCENT_PER_GROUP = "percent_per_group"
    SHOW_ORIGINAL = "show_original"
