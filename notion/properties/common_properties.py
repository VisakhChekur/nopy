from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from typing import Any
from typing import Optional
from typing import Type

from dateutil import parser as date_parser

from notion.exceptions import UnsupportedError
from notion.properties.base import BaseProperty
from notion.properties.prop_enums import Colors
from notion.properties.prop_enums import EmojiTypes
from notion.properties.prop_enums import FileTypes
from notion.properties.prop_enums import ParentTypes
from notion.properties.prop_enums import RichTextTypes


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

    def serialize_create(self) -> dict[str, Any]:

        return {"name": self.name, "color": self.color.value}

    def serialize_update(self) -> dict[str, Any]:

        # If a new database/page is being created or the property
        # is a new one on an existing database (implies 'id' is empty.)
        if not self.id:
            return self.serialize_create()
        return {"id": self.id, "color": self.color.value}

    @classmethod
    def from_dict(cls: Type[Option], args: dict[str, str]) -> Option:
        args["color"] = Colors[args["color"].upper()]  # type: ignore
        return Option(**args)


# TODO: Implement serialization.
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
    def from_dict(cls: Type[StatusGroup], args: dict[str, str]) -> StatusGroup:

        args["color"] = Colors[args["color"].upper()]  # type: ignore

        return StatusGroup(**args)


@dataclass
class Annotations(BaseProperty):
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

    @classmethod
    def from_dict(cls: Type[Annotations], args: dict[str, Any]) -> Annotations:
        if isinstance(args.get("color", None), str):
            args["color"] = Colors[args["color"].upper()]

        return Annotations(**args)

    def serialize_create(self) -> dict[str, Any]:
        return {
            "bold": self.bold,
            "italic": self.italic,
            "strikethrough": self.strikethrough,
            "underline": self.underline,
            "code": self.code,
            "color": self.color.value,
        }

    def serialize_update(self) -> dict[str, Any]:
        return self.serialize_create()


# TODO: Implement serialization.
class Link(BaseProperty):
    """A representation of a 'Link' object.

    Args:
        url:
    """

    def __init__(self, url: str):
        self.url = url

    @classmethod
    def from_dict(cls: Type[Link], args: dict[str, Any]) -> Link:
        return Link(args["url"])

    def serialize_create(self) -> dict[str, Any]:
        return {"type": "url", "url": self.url}

    def serialize_update(self) -> dict[str, Any]:
        return self.serialize_create()


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

    def serialize_create(self) -> dict[str, Any]:
        raise UnsupportedError("'mention' and 'equation' are not supported yet")

    def serialize_update(self) -> dict[str, Any]:
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

    def serialize_create(self) -> dict[str, Any]:

        if self.link:
            text = {"content": self.plain_text, "link": self.link.serialize_create()}
        else:
            text = {"content": self.plain_text}
        serialized = {
            "type": "text",
            "text": text,
            "annotations": self.annotations.serialize_create(),
        }
        return serialized

    def serialize_update(self) -> dict[str, Any]:
        return self.serialize_create()

    @classmethod
    def from_dict(cls: Type[Text], args: dict[str, Any]) -> Text:

        new_args: dict[str, Any] = {
            "plain_text": args["plain_text"],
            "href": args["href"],
            "link": args["text"]["link"],
            "annotations": Annotations.from_dict(args["annotations"]),
        }

        return Text(**new_args)


@dataclass
class File(BaseProperty):
    """A representation of a File object.

    Args:
        url (AnyUrl): The url of the file.
        type (FileType): The 'type' of file.
        expiry_time (datetime):
            The date on which the file will expire from Notion.
            NOTE: Only files hosted by Notion will have an `expiry_time`.
            That is, the `type` should be `FileType.FILE`.
    """

    url: str = ""
    expiry_time: Optional[datetime] = None
    type: FileTypes = FileTypes.EXTERNAL

    def serialize_create(self) -> dict[str, Any]:
        return {"type": self.type.value, self.type.value: {"url": self.url}}

    def serialize_update(self) -> dict[str, Any]:
        return self.serialize_create()

    @classmethod
    def from_dict(cls: Type[File], args: dict[str, Any]) -> File:

        file_type = args["type"]
        expiry = args[file_type].get("expiry_time", None)
        expiry_time = date_parser.parse(expiry) if expiry else None
        new_args: dict[str, Any] = {
            "type": FileTypes[file_type.upper()],
            "url": args[file_type]["url"],
            "expiry_time": expiry_time,
        }

        return File(**new_args)


@dataclass
class Emoji(BaseProperty):
    """A representation of the Emoji object.

    Args:
        emoji (str): The emoji as a Unicode string.
        type (EmojiTypes): The type of the emoji.
    """

    emoji: str

    def __post_init__(self):

        self.type = EmojiTypes.EMOJI

    def serialize_create(self) -> dict[str, Any]:
        return {"emoji": self.emoji}

    def serialize_update(self) -> dict[str, Any]:
        return self.serialize_create()

    @classmethod
    def from_dict(cls: Type[Emoji], args: dict[str, Any]) -> Emoji:
        return Emoji(args["emoji"])


@dataclass
class Parent(BaseProperty):

    id: str
    type: ParentTypes = ParentTypes.DATABASE

    def serialize_create(self) -> dict[str, Any]:
        return {self.type.value: self.id, "type": self.type.value}

    def serialize_update(self) -> dict[str, Any]:
        return self.serialize_create()


@dataclass
class DatabaseParent(Parent):
    def __post_init__(self):
        self.type = ParentTypes.DATABASE

    @classmethod
    def from_dict(cls: Type[DatabaseParent], args: dict[str, Any]) -> DatabaseParent:
        return DatabaseParent(args["database_id"])


@dataclass
class PageParent(Parent):
    def __post_init__(self):
        self.type = ParentTypes.PAGE

    @classmethod
    def from_dict(cls: Type[PageParent], args: dict[str, Any]) -> PageParent:
        return PageParent(args["page_id"])


@dataclass
class WorkspaceParent(Parent):

    id: str = ""

    def __post_init__(self):
        self.type = ParentTypes.WORKSPACE
        # For workspace parents, the id is marked as `True`
        # by the Notion API whereas all the otther parents IDs are strings.
        self.id = True  # type:ignore

    @classmethod
    def from_dict(cls: Type[WorkspaceParent], args: dict[str, Any]) -> WorkspaceParent:
        return WorkspaceParent()


@dataclass
class BlockParent(Parent):
    def __post_init__(self):
        self.type = ParentTypes.BLOCK

    @classmethod
    def from_dict(cls: Type[BlockParent], args: dict[str, Any]) -> BlockParent:
        return BlockParent(args["block_id"])
