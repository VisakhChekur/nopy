from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from typing import Any
from typing import Optional
from typing import Type
from zoneinfo import ZoneInfo

import dateutil.parser as date_parser

from ..exceptions import UnsupportedError
from .base import BaseProperty
from .prop_enums import Colors
from .prop_enums import EmojiTypes
from .prop_enums import FileTypes
from .prop_enums import ParentTypes
from .prop_enums import RichTextTypes


@dataclass
class Annotations(BaseProperty):
    """A representation of the annotations.

    Args:
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
        if isinstance(args.get("color", None), str):
            args["color"] = Colors[args["color"].upper()]

        return Annotations(**args)

    def serialize(self) -> dict[str, Any]:
        return {
            "bold": self.bold,
            "italic": self.italic,
            "strikethrough": self.strikethrough,
            "underline": self.underline,
            "code": self.code,
            "color": self.color.value,
        }


@dataclass
class Date(BaseProperty):
    """A representation of a date value in Notion.

    Args:
        start: The start time.
        end: The end time, if any.
        time_zone:
            The time zone, if any. If provided, the time provided
            in the `start` and `end` dates are ignored.
    """

    start: datetime
    end: Optional[datetime] = None
    time_zone: Optional[ZoneInfo] = None

    @classmethod
    def from_dict(cls: Type[Date], args: dict[str, Any]) -> Date:

        new_args: dict[str, Any] = {"start": date_parser.parse(args["start"])}
        if args["end"]:
            new_args["end"] = date_parser.parse(args["end"])
        if args["time_zone"]:
            new_args["time_zone"] = ZoneInfo(args["time_zone"])

        return Date(**new_args)


@dataclass
class Emoji(BaseProperty):
    """A representation of the Emoji object.

    Args:
        emoji: The emoji as a Unicode string.
        type (EmojiTypes): The type of the emoji.
    """

    emoji: str

    def __post_init__(self):

        self.type: EmojiTypes = EmojiTypes.EMOJI

    def serialize(self) -> dict[str, Any]:
        return {"emoji": self.emoji}

    @classmethod
    def from_dict(cls: Type[Emoji], args: dict[str, Any]) -> Emoji:
        return Emoji(args["emoji"])


@dataclass
class File(BaseProperty):
    """A representation of a File object.

    Args:
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
    name: str = ""

    def serialize(self) -> dict[str, Any]:
        return {"type": self.type.value, self.type.value: {"url": self.url}}

    @classmethod
    def from_dict(cls: Type[File], args: dict[str, Any]) -> File:

        file_type = args["type"]
        expiry = args[file_type].get("expiry_time", None)
        expiry_time = date_parser.parse(expiry) if expiry else None
        new_args: dict[str, Any] = {
            "type": FileTypes[file_type.upper()],
            "url": args[file_type]["url"],
            "expiry_time": expiry_time,
            "name": args.get("name", ""),
        }

        return File(**new_args)


class Link(BaseProperty):
    """A representation of a 'Link' object.

    Args:
        url: The url.
    """

    def __init__(self, url: str):
        self.url = url

    @classmethod
    def from_dict(cls: Type[Link], args: dict[str, Any]) -> Link:
        return Link(args["url"])

    def serialize(self) -> dict[str, Any]:
        return {"type": "url", "url": self.url}


@dataclass
class Option(BaseProperty):
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

    def serialize(self) -> dict[str, Any]:

        return {"name": self.name, "color": self.color.value}

    @classmethod
    def from_dict(cls: Type[Option], args: dict[str, Any]) -> Option:
        args["color"] = Colors[args["color"].upper()]
        return Option(**args)


@dataclass
class StatusGroup(BaseProperty):
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
    option_ids: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls: Type[StatusGroup], args: dict[str, Any]) -> StatusGroup:

        args["color"] = Colors[args["color"].upper()]

        return StatusGroup(**args)

    def serialize(self) -> dict[str, Any]:
        raise UnsupportedError(
            "updation/creation of `Status Group` is not supported by the official Notion API"
        )


@dataclass
class RichText(BaseProperty):
    """Base class of Rich Text.

    Args:
        plain_text: The text without any annotations.
        annotations: The annotations applied on the text.
        href: The link, if any, within the text.
        type: The 'type' of the Rich Text.
    """

    plain_text: str
    href: Optional[str] = None
    annotations: Annotations = field(default_factory=Annotations)

    def __post_init__(self):

        self.type = RichTextTypes.UNSUPPORTED
        self.plain_text = self.plain_text.strip()

    def serialize(self) -> dict[str, Any]:
        raise UnsupportedError("'mention' and 'equation' are not supported yet")

    @classmethod
    def from_dict(cls: Type[RichText], args: dict[str, Any]) -> RichText:

        new_args: dict[str, Any] = {
            "annotations": Annotations.from_dict(args["annotations"]),
            "plain_text": args["plain_text"],
            "href": args["href"],
        }
        return RichText(**new_args)


@dataclass
class Text(RichText):
    """A representation of 'Text' type of Rich Text.

    Args:
        plain_text: The text without any annotations.
        annotations: The annotations applied on the text.
        href: The link, if any, within the text.
        type: The 'type' of the Rich Text.
        link:
            Any inline link within the text. This should be the one used
            by the user when creating a new property or updating an
            existing property instead of `href`.
    """

    link: Optional[Link] = None

    def __post_init__(self):

        self.plain_text = self.plain_text.strip()
        self.type = RichTextTypes.TEXT

    def serialize(self) -> dict[str, Any]:

        if self.link:
            text = {"content": self.plain_text, "link": self.link.serialize()}
        else:
            text = {"content": self.plain_text}
        serialized = {
            "type": "text",
            "text": text,
            "annotations": self.annotations.serialize(),
        }
        return serialized

    @classmethod
    def from_dict(cls: Type[Text], args: dict[str, Any]) -> Text:

        new_args: dict[str, Any] = {
            "plain_text": args["plain_text"],
            "href": args["href"],
            "annotations": Annotations.from_dict(args["annotations"]),
        }
        if args["text"].get("link", None):
            new_args["link"] = Link.from_dict(args["text"]["link"])
        return Text(**new_args)


@dataclass
class Parent(BaseProperty):
    """A representation of a parent of a Notion object.

    The base parent class from which all parent objects inherit.

    Args:
        id: The id of the parent.
        type: The type of the parent.
    """

    id: str

    def __post_init__(self):
        self._type = ParentTypes.UNSUPPORTED

    @property
    def type(self):
        return self._type

    def serialize(self) -> dict[str, Any]:
        if self._type == ParentTypes.UNSUPPORTED:
            raise UnsupportedError("this parent type is not supported")

        return {self._type.value: self.id, "type": self._type.value}


@dataclass
class DatabaseParent(Parent):
    """A representation of a database parent of a Notion object.

    Args:
        id: The id of the database.
        type: The type of the parent which is always `ParentTypes.DATABASE`.
    """

    def __post_init__(self):
        self._type = ParentTypes.DATABASE

    @classmethod
    def from_dict(cls: Type[DatabaseParent], args: dict[str, Any]) -> DatabaseParent:
        return DatabaseParent(args["database_id"])


@dataclass
class PageParent(Parent):
    """A representation of a page parent of a Notion object.

    Args:
        id: The id of the page.
        type: The type of the parent which is always `ParentTypes.PAGE`.
    """

    def __post_init__(self):
        self._type = ParentTypes.PAGE

    @classmethod
    def from_dict(cls: Type[PageParent], args: dict[str, Any]) -> PageParent:
        return PageParent(args["page_id"])


@dataclass
class WorkspaceParent(Parent):
    """A representation of a workspace parent of a Notion object.

    Args:
        id: The id of the workspace.
        type: The type of the parent which is always `ParentTypes.WORKSPACE`.
    """

    id: str = ""

    def __post_init__(self):
        self._type = ParentTypes.WORKSPACE
        # For workspace parents, the id is marked as `True`
        # by the Notion API whereas all the otther parents IDs are strings.
        self.id = True  # type:ignore

    @classmethod
    def from_dict(cls: Type[WorkspaceParent], args: dict[str, Any]) -> WorkspaceParent:
        return WorkspaceParent()


@dataclass
class BlockParent(Parent):
    """A representation of a block parent of a Notion object.

    Args:
        id: The id of the block.
        type: The type of the parent which is always `ParentTypes.BLOCK`.
    """

    def __post_init__(self):
        self._type = ParentTypes.BLOCK

    @classmethod
    def from_dict(cls: Type[BlockParent], args: dict[str, Any]) -> BlockParent:
        return BlockParent(args["block_id"])