from dataclasses import InitVar, dataclass, field
from datetime import datetime
from typing import Any, Literal, Optional, Union
from dateutil import parser as date_parser

from notion.properties.types_enums import RichTextTypes, Colors, FileTypes, EmojiTypes
from notion.properties.types_enums import RICH_TEXT_TYPES_REVERSE_MAP, COLORS_REVERSE_MAP, FILE_TYPES_REVERSE_MAP
from notion.exceptions import UnsupportedError

UNSUPPORTED_PROPS = Literal["relation", "rollup", "formula"]

# TODO: Validate inputs before all serializations to reduce invalid calls to Notion API

@dataclass
class Annotations:
    """Represents 'annotations'.
    
    Args:
        bold: Text is bold.
        italic: Text is italicized.
        strikethrough: Text is striked through.
        underline: Text is underlined.
        code: Text is in code style.
    """

    bold: bool = False
    italic: bool = False
    strikethrough: bool = False
    underline: bool = False
    code: bool = False
    color: Colors = Colors.DEFAULT

    def serialize(self) -> dict[str, bool]:
        """Serializes the instance into dictionary following Notion spec."""

        return self.__dict__

    @classmethod
    def from_dict(cls, annotations_dict: dict[str, Any]) -> "Annotations":

        if "color" in annotations_dict:
            annotations_dict["color"] = COLORS_REVERSE_MAP[annotations_dict["color"]]
        return Annotations(**annotations_dict)


@dataclass
class RichText:
    """Represents 'rich_text' type. 
    
    Args:
        plain_text: The text as plain text without any annotations.
        annotations: The annotations to apply on the text.
        href: The URL of any link or internal Notion mention in this text.
        type: The 'rich_text' type. Currently only 'text' is supported.
    """

    plain_text: str
    annotations: Annotations = field(default_factory=Annotations)
    href: str = ""
    type: RichTextTypes = RichTextTypes.TEXT

    def serialize(self) -> dict[str, Any]:
        """Serializes the instance into dictionary following Notion spec."""

        text: dict[str, Any] = {"content": self.plain_text}
        if self.href:
            text["link"] = {
                "url": self.href
            }
        return {
            "annotations": self.annotations.serialize(),
            "type": self.type.value,
            "text": text
        }
    
    @classmethod
    def from_dict(cls, rich_text_dict: dict[str, Any]) -> "RichText":

        rich_text_dict["annotations"] = Annotations.from_dict(rich_text_dict["annotations"])
        rich_text_type = rich_text_dict["type"]
        rich_text_dict["type"] = RICH_TEXT_TYPES_REVERSE_MAP[rich_text_type]
        rich_text_dict.pop(rich_text_type)
        return RichText(**rich_text_dict)

@dataclass
class Option:
    """A representation of an option.
    
    This can be used for 'Select', 'Status' and 'Multi-select'.    
    """

    name: str
    color: Colors = Colors.DEFAULT
    id: str = ""

    def __post_init__(self):

        if "," in self.name:
            raise ValueError("',' are not allowed in names of select options")
    
    def serialize(self, with_id:bool=False) -> dict[str, str]:

        serialized = {
            "color": self.color.value
        }
        if with_id:
            serialized["id"] = self.id
        else:
            serialized["name"] = self.name
        
        return serialized

    @classmethod
    def from_dict(cls, option_dict: dict[str, Any]) -> "Option":

        return Option(**option_dict)

@dataclass
class StatusGroup:

    name: str
    color: Colors = Colors.DEFAULT
    id: str = ""
    # TODO: Find out what the hell these are
    option_ids: list[str] = field(default_factory=list)

    def serialize(self, with_id: bool = False) -> dict[str, str | list[str]]:

        serialized: dict[str, str | list[str]] = {
            "color": self.color.value,
            "option_ids": sorted(self.option_ids)
        }
        if with_id:
            serialized["id"] = self.id
        else:
            serialized["name"] = self.name
        
        return serialized
    
    @classmethod
    def from_dict(cls, status_group_dict: dict[str, Any]) -> "StatusGroup":

        return StatusGroup(**status_group_dict)
    
@dataclass
class File:

    url: str
    type: FileTypes = FileTypes.EXTERNAL
    file_expiry_time: InitVar[Optional[Union[str, datetime]]] = None

    def __post_init__(self, file_expiry_time: Optional[Union[str, datetime]]):

        self.expiry_time: Optional[datetime]
        if not file_expiry_time:
            self.expiry_time = None
        elif isinstance(file_expiry_time, str):
            self.expiry_time = date_parser.parse(file_expiry_time)
        else:
            self.expiry_time = file_expiry_time

    def serialize(self):

        if self.type == FileTypes.FILE:
            raise UnsupportedError("uploading files via the API is unuspported by the official Notion API")
        return {
            "type": self.type.value,
            self.type.value: self.url
        }

    @classmethod
    def from_dict(cls, file_dict: dict[str, Any]) -> "File":

        file_type = file_dict["type"]
        return File(
            **file_dict[file_type],
            FILE_TYPES_REVERSE_MAP[file_type], # type: ignore
        )
        

@dataclass
class Emoji:

    emoji: str

    def __post_init__(self):
        self.type = EmojiTypes.EMOJI
    
    def serialize(self):

        if not self.emoji:
            raise ValueError("'emoji' attribute can't be empty")
        
        return {
            "emoji": self.emoji
        }
    @classmethod
    def from_dict(cls, emoji_dict: dict[str, Any]) -> "Emoji":
        pass


@dataclass
class User:
    # TODO: Implement User.
    pass