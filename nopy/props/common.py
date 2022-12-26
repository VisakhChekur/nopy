from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from typing import Any
from typing import Optional
from typing import Type
from zoneinfo import ZoneInfo

from dateutil.parser import parse

from nopy.enums import Colors
from nopy.enums import FileTypes
from nopy.enums import MentionTypes
from nopy.enums import ParentTypes
from nopy.enums import RichTextTypes
from nopy.errors import UnsupportedByNotion
from nopy.objects.user import User
from nopy.props.base import BaseProperty


@dataclass
class Annotations(BaseProperty):
    """A representation of the annotations.

    Attributes:
        bold: Mark the text as bold.
        italic: Make the text italic.
        strikethrough: Strikethrough the text.
        underline: Underline the text.
        code: Mark the text as code.
        color: Change the color of the code.
    """

    bold: bool = False
    italic: bool = False
    strikethrough: bool = False
    underline: bool = False
    code: bool = False
    color: Colors = Colors.DEFAULT

    @classmethod
    def from_dict(cls: Type[Annotations], args: dict[str, Any]) -> Annotations:

        new_args: dict[str, Any] = args.copy()
        new_args["color"] = Colors[new_args["color"].upper()]
        return Annotations(**new_args)

    def serialize(self) -> dict[str, Any]:

        serialized = self.__dict__.copy()
        serialized["color"] = self.color.value
        return serialized


@dataclass
class Date(BaseProperty):
    """A representation of a date in Notion.

    Attributes:
        start: The start date and time.
        end: The end date and time, if any.
        time_zone: The time zone, if any.
    """

    start: datetime
    end: Optional[datetime] = None
    time_zone: Optional[ZoneInfo] = None

    def serialize(self) -> dict[str, Any]:

        return {
            "start": self.start.isoformat(),
            "end": None if self.end is None else self.end.isoformat(),
            "time_zone": None if self.time_zone is None else str(self.time_zone),
        }

    @classmethod
    def from_dict(cls: Type[Date], args: dict[str, Any]) -> Date:

        start = parse(args["start"])
        end = None
        time_zone = None
        if end_str := args["end"]:
            end = parse(end_str)
        if tz := args["time_zone"]:
            time_zone = ZoneInfo(tz)

        return Date(start, end, time_zone)


@dataclass
class Link(BaseProperty):
    """A representation of a link object.

    Attributes:
        url: The URL.
    """

    url: str

    @classmethod
    def from_dict(cls: Type[Link], args: dict[str, Any]) -> Link:
        return Link(args["url"])

    def serialize(self) -> dict[str, Any]:
        return {"url": self.url}


@dataclass
class RichText(BaseProperty):
    """A represenation of a rich text property.

    Attributes:
        plain_text: The plain text without any annotations/styling.
        href: The URL to the link, if any.
        annotations: The annotations/styles applied on this text.
        type (RichTextTypes):
            The type of rich text which will always be
            `RichText.UNSUPPORTED`.
    """

    plain_text: str = ""
    href: str = ""
    annotations: Annotations = field(default_factory=Annotations)

    def __post_init__(self):

        # Notion adds spaces within the plain text
        self.plain_text = self.plain_text.strip()
        self._type: RichTextTypes = RichTextTypes.UNSUPPORTED

    @property
    def type(self) -> RichTextTypes:
        return self._type

    @classmethod
    def from_dict(cls: Type[RichText], args: dict[str, Any]) -> RichText:

        try:
            rich_text_type = RichTextTypes[args["type"].upper()]
        except KeyError:
            rich_text_type = RichTextTypes.UNSUPPORTED

        if rich_text_type == RichTextTypes.TEXT:
            return Text.from_dict(args)
        if rich_text_type == RichTextTypes.MENTION:
            return Mention.from_dict(args)
        if rich_text_type == RichTextTypes.EQUATION:
            return Equation.from_dict(args)

        base = _rich_text_base_args(args)
        return RichText(**base)


@dataclass
class Text(RichText):
    """A represenation of a text type of rich text.

    Attributes:
        plain_text (str): The plain text without any annotations/styling.
        href (str): The URL to the link, if any.
        annotations (Annotations): The annotations/styles applied on this text.
        link: The link within the text, if any.
        type (RichTextTypes):
            The type of rich text which will always be
            `RichText.UNSUPPORTED`.
    """

    link: Optional[Link] = None

    def __post_init__(self):

        self.plain_text = self.plain_text.strip()
        self._type = RichTextTypes.TEXT

    @classmethod
    def from_dict(cls: Type[Text], args: dict[str, Any]) -> Text:

        new_args = _rich_text_base_args(args)
        link = args[RichTextTypes.TEXT.value].get("link", None)
        if link:
            new_args["link"] = Link.from_dict(link)
        return Text(**new_args)

    def serialize(self) -> dict[str, Any]:

        serialized: dict[str, Any] = {
            "type": self._type.value,
            self._type.value: {
                "content": self.plain_text + " ",
            },
            "annotations": self.annotations.serialize(),
        }
        if self.link:
            serialized["link"] = self.link.serialize()
        return serialized


@dataclass
class Mention(RichText):
    """A represenation of a mention type of rich text.

    Attributes:
        plain_text (str): The plain text without any annotations/styling.
        mention_type:
            The type of the mention. Available attributes depend on this
            type.
        id: The id of the mention, if any.
        user: The mention user, if any.
        date: The date mentioned, if any.
        url: The URL mentioned, if any.
        href (str): The URL to the link, if any.
        annotations (Annotations): The annotations/styles applied on this text.
        type (RichTextTypes):
            The type of rich text which will always be
            `RichText.UNSUPPORTED`.
    """

    mention_type: MentionTypes = MentionTypes.UNSUPPORTED
    user: Optional[User] = None
    id: str = ""
    date: Optional[Date] = None
    url: Optional[str] = None

    def __post_init__(self):

        super().__post_init__()
        self._type = RichTextTypes.MENTION

    @classmethod
    def from_dict(cls: Type[Mention], args: dict[str, Any]) -> Mention:

        new_args: dict[str, Any] = _rich_text_base_args(args)
        try:
            mention_type = MentionTypes[args["mention"]["type"].upper()]
        except KeyError:
            mention_type = MentionTypes.UNSUPPORTED
            new_args["mention_type"] = mention_type
            return Mention(**new_args)

        new_args["mention_type"] = mention_type
        mention_details = args[RichTextTypes.MENTION.value]
        if mention_type == MentionTypes.DATE:
            new_args["date"] = Date.from_dict(mention_details["date"])
        elif mention_type == MentionTypes.LINK_PREVIEW:
            new_args["url"] = mention_details["url"]
        elif mention_type == MentionTypes.USER:
            new_args["user"] = User.from_dict(mention_details[mention_type.value])
        elif mention_type in (MentionTypes.DATABASE, MentionTypes.PAGE):
            new_args["id"] = mention_details[mention_type.value]["id"]

        return Mention(**new_args)


@dataclass
class Equation(RichText):
    """A represenation of an equation type of rich text.

    Attributes:
        plain_text (str): The plain text without any annotations/styling.
        expression: The mathematical expression as a LaTeX string.
        href (str): The URL to the link, if any.
        annotations (Annotations): The annotations/styles applied on this text.
        type (RichTextTypes):
            The type of rich text which will always be
            `RichText.UNSUPPORTED`.
    """

    expression: str = ""

    def __post_init__(self):

        super().__post_init__()
        self._type = RichTextTypes.EQUATION

    @classmethod
    def from_dict(cls: Type[Equation], args: dict[str, Any]) -> Equation:

        new_args = _rich_text_base_args(args)
        new_args["expression"] = args[RichTextTypes.EQUATION.value]["expression"]
        return Equation(**new_args)


@dataclass
class File(BaseProperty):
    """A representation of a File object.

    Attributes:
        url: The url of the file.
        type (FileTypes): The 'type' of file.
        expiry_time:
            The date on which the file will expire from Notion.
            NOTE: Only files hosted by Notion will have an `expiry_time`.
            That is, the `type` should be `FileType.FILE`.
    """

    url: str = ""
    expiry_time: Optional[datetime] = None
    type: FileTypes = FileTypes.EXTERNAL

    @classmethod
    def from_dict(cls: Type[File], args: dict[str, Any]) -> File:

        file_type = FileTypes[args["type"].upper()]
        file_details = args[file_type.value]

        new_args: dict[str, Any] = {
            "url": file_details["url"],
            "type": file_type,
        }

        # Only files hosted by Notion have expiry dates
        if file_type == FileTypes.FILE:
            new_args["expiry_time"] = parse(file_details["expiry_time"])

        return File(**new_args)

    def serialize(self) -> dict[str, Any]:

        if self.type == FileTypes.FILE:
            msg = "uploading local files"
            raise UnsupportedByNotion(msg)

        return {
            "type": self.type.value,
            self.type.value: {
                "url": self.url,
            },
        }


@dataclass
class Option(BaseProperty):
    """A representation of an Option.

    This can be used in the options for Select and Multi-Select
    properties.

    Attributes:
        name: Name of the option.
        id: Id of the option.
        color: The color associated with the option.
    """

    name: str
    id: str = ""
    color: Colors = Colors.DEFAULT

    @classmethod
    def from_dict(cls: Type[Option], args: dict[str, Any]) -> Option:
        args["color"] = Colors[args["color"].upper()]
        return Option(**args)

    def serialize(self) -> dict[str, Any]:
        return {"name": self.name, "color": self.color.value}


@dataclass
class StatusGroup(BaseProperty):
    """A representation of a Status Group.

    Attributes:
        name: Name of the group.
        id: Id of the group.
        color: Color associated with the group.
        option_ids: The list of option ids associated with the group.
    """

    name: str
    id: str = ""
    color: Colors = Colors.DEFAULT
    option_ids: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls: Type[StatusGroup], args: dict[str, Any]) -> StatusGroup:

        args["color"] = Colors[args["color"].upper()]

        return StatusGroup(**args)


@dataclass
class Emoji(BaseProperty):
    """A representation of the Emoji object.

    Attributes:
        emoji: The emoji as a Unicode string.
    """

    emoji: str

    @classmethod
    def from_dict(cls: Type[Emoji], args: dict[str, Any]) -> Emoji:
        return Emoji(args["emoji"])

    def serialize(self) -> dict[str, Any]:
        return {"emoji": self.emoji, "type": "emoji"}


@dataclass
class Parent(BaseProperty):
    """A representation of a parent of a Notion object.

    The base parent class from which all parent objects inherit.

    Attributes:
        id: The id of the parent.
        type (ParentTypes):
            The type of the parent which will always be
            `ParentTypes.UNSUPPORTED`.
    """

    id: str = ""

    def __post_init__(self):
        self._type = ParentTypes.UNSUPPORTED

    @classmethod
    def from_dict(cls: Type[Parent], args: dict[str, Any]) -> Parent:

        try:
            type_key = args["type"].split("_")[0]
            parent_type = ParentTypes[type_key.upper()]
        except KeyError:
            parent_type = ParentTypes.UNSUPPORTED

        if parent_type == ParentTypes.DATABASE:
            return DatabaseParent.from_dict(args)
        if parent_type == ParentTypes.PAGE:
            return PageParent.from_dict(args)
        if parent_type == ParentTypes.BLOCK:
            return BlockParent.from_dict(args)
        if parent_type == ParentTypes.WORKSPACE:
            return WorkspaceParent.from_dict(args)

        return Parent("")

    def serialize(self) -> dict[str, Any]:

        if self._type == ParentTypes.UNSUPPORTED:
            return super().serialize()

        return {
            "type": self._type.value,
            self._type.value: self.id,
        }


@dataclass
class DatabaseParent(Parent):
    """A representation of a database parent of a Notion object.

    Attributes:
        id (str): The id of the database.
        type (ParentTypes):
            The type of the parent which will always
            be `ParentTypes.DATABASE`.
    """

    def __post_init__(self):
        self._type = ParentTypes.DATABASE

    @classmethod
    def from_dict(cls: Type[DatabaseParent], args: dict[str, Any]) -> DatabaseParent:
        return DatabaseParent(args[ParentTypes.DATABASE.value])


@dataclass
class PageParent(Parent):
    """A representation of a page parent of a Notion object.

    Attributes:
        id (str): The id of the page.
        type (ParentTypes):
            The type of the parent which will always
            be `ParentTypes.PAGE`.
    """

    def __post_init__(self):
        self._type = ParentTypes.PAGE

    @classmethod
    def from_dict(cls: Type[PageParent], args: dict[str, Any]) -> PageParent:
        return PageParent(args[ParentTypes.PAGE.value])


@dataclass
class WorkspaceParent(Parent):
    """A representation of a workspace parent of a Notion object.

    Attributes:
        id (str): The id of the workspace.
        type (ParentType): The type of the parent which will always
            be `ParentTypes.WORKSPACE`.
    """

    id: str = ParentTypes.WORKSPACE.value

    def __post_init__(self):
        self._type = ParentTypes.WORKSPACE
        # For workspace parents, the id is marked as `True`
        # by the Notion API whereas all the otther parents IDs are strings.

    @classmethod
    def from_dict(cls: Type[WorkspaceParent], args: dict[str, Any]) -> WorkspaceParent:
        return WorkspaceParent(args[ParentTypes.WORKSPACE.value])


@dataclass
class BlockParent(Parent):
    """A representation of a block parent of a Notion object.

    Attributes:
        id (str): The id of the block.
        type (ParentTypes): The type of the parent which will always
            be `ParentTypes.BLOCK`.
    """

    def __post_init__(self):
        self._type = ParentTypes.BLOCK

    @classmethod
    def from_dict(cls: Type[BlockParent], args: dict[str, Any]) -> BlockParent:
        return BlockParent(args[ParentTypes.BLOCK.value])


# ----- Helper functions for `from_dict` -----
def _rich_text_base_args(args: dict[str, Any]) -> dict[str, Any]:

    return {
        "plain_text": args["plain_text"],
        "href": args["href"],
        "annotations": Annotations.from_dict(args["annotations"]),
    }
