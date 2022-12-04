from dataclasses import InitVar
from typing import TYPE_CHECKING
from typing import Any
from typing import Optional

from dateutil import parser as date_parser
from pydantic import AnyUrl
from pydantic import Field
from pydantic import validator
from pydantic.dataclasses import dataclass

from notion.properties.prop_enums import Colors
from notion.properties.prop_enums import EmojiTypes
from notion.properties.prop_enums import FileTypes
from notion.properties.prop_enums import ParentTypes
from notion.properties.prop_enums import RichTextTypes

if TYPE_CHECKING:
    from notion.typings import OptionalDict


@dataclass
class Option:
    """A representation of an Option.

    This can be used in the options for Select, Mutli-select
    and Status options.

    Args:
        name: Name of the option.
        id: Id of the option.
        color: The color associated with the option.
    """

    name: str
    id: str = ""
    color: Colors = Colors.DEFAULT

    @validator("name")
    def _check_name(cls, v: str):
        if "," in v:
            raise ValueError("',' is not allowed in option names")
        return v


@dataclass
class StatusGroup:
    """A representation of a Status Group.

    Args:
        name: Name of the group.
        id: Id of the group.
        color: Color associated with the group.
        option_ids: The list of option ids associated with the group.
    """

    name: str
    id: str = ""
    color: Colors = Colors.DEFAULT
    option_ids: list[str] = Field(default_factory=list)


@dataclass
class Annotations:
    """A representation of the annotations.

    Args:
        bold:
        italic:
        strikethrough:
        underline:
        code:
        color:
    """

    bold: bool = False
    italic: bool = False
    strikethrough: bool = False
    underline: bool = False
    code: bool = False
    color: Colors = Colors.DEFAULT


@dataclass
class Link:
    """A representation of a 'Link' object.

    Args:
        url:
    """

    url: Optional[AnyUrl] = None


@dataclass
class RichText:
    """Base class of Rich Text.

    Args:
        plain_text: The text without any annotations.
        annotations: The annotations applied on the text.
        href: The link, if any, within the text.
        type: The 'type' of the Rich Text.
    """

    plain_text: str
    href: Optional[str] = None
    annotations: Annotations = Field(default_factory=Annotations)

    def __post_init__(self):

        self.type = RichTextTypes.UNSUPPORTED
        self.plain_text = self.plain_text.strip()


@dataclass
class Text(RichText):
    """A representation of 'Text' type of Rich Text.

    Args:
        plain_text: The text without any annotations.
        annotations: The annotations applied on the text.
        href: The link, if any, within the text.
        type: The 'type' of the Rich Text.
        link: Any inline link within the text.
    """

    text: InitVar["OptionalDict"] = None
    link: Optional[Link] = None

    def __post_init__(self, text: Optional[dict[str, Any]]):  # type: ignore

        if text:
            self.link = Link(**text)

        self.type = RichTextTypes.TEXT


@dataclass
class File:
    """A representation of a File object.

    Args:
        url (AnyUrl): The url of the file.
        type (FileType): The 'type' of file.
        expiry_time (datetime):
            The date on which the file will expire from Notion.
            NOTE: Only files hosted by Notion will have an `expiry_time`.
            That is, the `type` should be `FileType.FILE`.
    """

    url: Optional[AnyUrl] = None
    file: InitVar["OptionalDict"] = None
    external: InitVar["OptionalDict"] = None
    type: FileTypes = FileTypes.EXTERNAL

    def __post_init__(self, file: "OptionalDict", external: "OptionalDict"):

        if not self.url and not file and not external:
            raise TypeError("provide 'url', and one of 'file', or 'external'")
        if file:
            self.url = file["url"]
            self.type = FileTypes.FILE
            self.expiry_time = date_parser.parse(file["expiry_time"])
        else:
            self.url = external["url"]  # type: ignore
            self.type = FileTypes.EXTERNAL
            self.expiry_time = None


@dataclass
class Emoji:
    """A representation of the Emoji object.

    Args:
        emoji (str): The emoji as a Unicode string.
        type (EmojiTypes): The type of the emoji.
    """

    emoji: str

    def __post_init__(self):

        self.type = EmojiTypes.EMOJI


@dataclass
class Parent:

    type: ParentTypes


@dataclass
class DatabaseParent(Parent):

    database_id: str


@dataclass
class PageParent(Parent):

    page_id: str


@dataclass
class WorkspaceParent(Parent):

    workspace: str


@dataclass
class BlockParent(Parent):

    block_id: str
