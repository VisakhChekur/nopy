from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import TYPE_CHECKING
from typing import Any
from typing import ClassVar
from typing import Optional
from typing import Type
from typing import Union

from nopy.enums import BlockTypes
from nopy.enums import Colors
from nopy.enums import HeadingLevel
from nopy.enums import ListTypes
from nopy.enums import MediaTypes
from nopy.enums import ObjectTypes
from nopy.errors import NoClientFoundError
from nopy.objects.notion_object import NotionObject
from nopy.props.common import Emoji
from nopy.props.common import File
from nopy.props.common import RichText
from nopy.utils import TextDescriptor
from nopy.utils import block_base_args
from nopy.utils import get_icon
from nopy.utils import paginate
from nopy.utils import rich_text_color_mixin_args
from nopy.utils import rich_text_list

if TYPE_CHECKING:
    from nopy.objects.database import Database
    from nopy.objects.page import Page


MEDIA_TYPES = tuple((mt.value for mt in MediaTypes))


@dataclass
class Block(NotionObject):

    has_children: bool = False

    def __post_init__(self):
        super().__post_init__()
        self._type = ObjectTypes.BLOCK
        self._block_type = BlockTypes.UNSUPPORTED

    @property
    def block_type(self) -> BlockTypes:
        return self._block_type

    def get_children(self):

        if not self._client:
            raise NoClientFoundError("no client was set")

        return paginate(
            self._client._retrieve_block_children,  # type: ignore
            Block.from_dict,
            client=self._client,
            block_id=self.id,
        )

    def delete(self):
        """Deletes the block."""

        if not self._client:
            raise NoClientFoundError("no client was set")

    @classmethod
    def from_dict(cls: Type[Block], args: dict[str, Any]) -> Block:

        raw_block_type: str = args["type"]
        try:
            block_type = BlockTypes[raw_block_type.upper()]
        except KeyError:
            if raw_block_type.startswith("heading"):
                block_type = BlockTypes.HEADING
            elif raw_block_type.endswith("list_item"):
                block_type = BlockTypes.LIST
            elif raw_block_type in MEDIA_TYPES:
                block_type = BlockTypes.MEDIA
            else:
                block_type = BlockTypes.UNSUPPORTED

        if block_type == BlockTypes.UNSUPPORTED:
            return Block(**block_base_args(args))

        block_type = _BLOCK_REVERSE_MAP[block_type]
        return block_type.from_dict(args)


# Yes, the name is atrocious.
@dataclass
class _BlockRichTextAndColorMixin:

    text: ClassVar[TextDescriptor] = TextDescriptor("rich_text")

    rich_text: list[RichText] = field(default_factory=list)
    color: Colors = Colors.DEFAULT


@dataclass
class Paragraph(Block, _BlockRichTextAndColorMixin):
    def __post_init__(self):

        super().__post_init__()
        self._block_type = BlockTypes.PARAGRAPH

    @classmethod
    def from_dict(cls: Type[Paragraph], args: dict[str, Any]) -> Paragraph:

        new_args = rich_text_color_mixin_args(args[BlockTypes.PARAGRAPH.value])
        new_args.update(block_base_args(args))

        return Paragraph(**new_args)


@dataclass
class Heading(Block, _BlockRichTextAndColorMixin):

    is_toggleable: bool = False
    heading_level: HeadingLevel = HeadingLevel.HEADING_1

    def __post_init__(self):
        super().__post_init__()
        self._block_type = BlockTypes.HEADING

    @classmethod
    def from_dict(cls: Type[Heading], args: dict[str, Any]) -> Heading:

        heading_level = args["type"]
        heading = args[heading_level]
        new_args: dict[str, Any] = {
            "is_toggleable": heading["is_toggleable"],
            "heading_level": HeadingLevel[heading_level.upper()],
        }
        new_args.update(block_base_args(args))
        new_args.update(rich_text_color_mixin_args(heading))

        return Heading(**new_args)


@dataclass
class Callout(Block, _BlockRichTextAndColorMixin):

    icon: Optional[Union[File, Emoji]] = None

    def __post_init__(self):
        super().__post_init__()
        self._block_type = BlockTypes.CALLOUT

    @classmethod
    def from_dict(cls: Type[Block], args: dict[str, Any]) -> Block:

        callout = args[BlockTypes.CALLOUT.value]
        new_args: dict[str, Any] = {
            "icon": get_icon(callout["icon"]),
        }
        new_args.update(block_base_args(args))
        new_args.update(rich_text_color_mixin_args(callout))

        return Callout(**new_args)


@dataclass
class Quote(Block, _BlockRichTextAndColorMixin):
    def __post_init__(self):

        super().__post_init__()
        self._block_type = BlockTypes.QUOTE

    @classmethod
    def from_dict(cls: Type[Quote], args: dict[str, Any]) -> Quote:

        quote = args["quote"]
        new_args: dict[str, Any] = {
            "color": Colors[quote["color"].upper()],
            "rich_text": rich_text_list(quote["rich_text"]),
        }
        new_args.update(block_base_args(args))
        new_args.update(rich_text_color_mixin_args(quote))

        return Quote(**new_args)


@dataclass
class List(Block, _BlockRichTextAndColorMixin):

    list_type: ListTypes = ListTypes.BULLETED_LIST_ITEM

    def __post_init__(self):

        super().__post_init__()
        self._block_type = BlockTypes.LIST

    @classmethod
    def from_dict(cls: Type[List], args: dict[str, Any]) -> List:

        list_type = args["type"]
        list_ = args[list_type]
        new_args: dict[str, Any] = {"list_type": ListTypes[list_type.upper()]}
        new_args.update(block_base_args(args))
        new_args.update(rich_text_color_mixin_args(list_))

        return List(**new_args)


@dataclass
class Todo(Block, _BlockRichTextAndColorMixin):

    checked: bool = False

    def __post_init__(self):
        super().__post_init__()
        self._block_type = BlockTypes.TO_DO

    @classmethod
    def from_dict(cls: Type[Todo], args: dict[str, Any]) -> Todo:

        todo = args[BlockTypes.TO_DO.value]
        new_args = {"checked": todo["checked"]}
        new_args.update(rich_text_color_mixin_args(todo))
        new_args.update(block_base_args(args))

        return Todo(**new_args)


@dataclass
class Toggle(Block, _BlockRichTextAndColorMixin):
    def __post_init__(self):
        super().__post_init__()
        self._block_type = BlockTypes.TOGGLE

    @classmethod
    def from_dict(cls: Type[Toggle], args: dict[str, Any]) -> Toggle:

        new_args = rich_text_color_mixin_args(args[BlockTypes.TOGGLE.value])
        new_args.update(block_base_args(args))

        return Toggle(**new_args)


@dataclass
class Code(Block):

    code: ClassVar[TextDescriptor] = TextDescriptor("rich_code")
    caption: ClassVar[TextDescriptor] = TextDescriptor("rich_caption")

    rich_code: list[RichText] = field(default_factory=list)
    rich_caption: list[RichText] = field(default_factory=list)
    language: str = "python"

    def __post_init__(self):
        super().__post_init__()
        self._block_type = BlockTypes.CODE

    @classmethod
    def from_dict(cls: Type[Code], args: dict[str, Any]) -> Code:

        code = args[BlockTypes.CODE.value]
        new_args: dict[str, Any] = {
            "rich_caption": rich_text_list(code["caption"]),
            "rich_code": rich_text_list(code["rich_text"]),
            "language": code["language"],
        }
        new_args.update(block_base_args(args))

        return Code(**new_args)


@dataclass
class ChildPage(Block):

    title: str = ""

    def __post_init__(self):
        super().__post_init__()
        self._block_type = BlockTypes.CHILD_PAGE

    def get_page(self) -> "Page":

        if not self._client:
            raise NoClientFoundError("no client has been set")

        return self._client.retrieve_page(self.id)

    @classmethod
    def from_dict(cls: Type[ChildPage], args: dict[str, Any]) -> ChildPage:

        new_args = {
            "title": args[BlockTypes.CHILD_PAGE.value]["title"],
        }
        new_args.update(block_base_args(args))

        return ChildPage(**new_args)


@dataclass
class ChildDatabase(Block):

    title: str = ""

    def __post_init__(self):
        super().__post_init__()
        self._block_type = BlockTypes.CHILD_DATABASE

    def get_db(self) -> "Database":

        if not self._client:
            raise NoClientFoundError("no client has been set")

        return self._client.retrieve_db(self.id)

    @classmethod
    def from_dict(cls: Type[ChildDatabase], args: dict[str, Any]) -> ChildDatabase:

        new_args = {
            "title": args[BlockTypes.CHILD_DATABASE.value]["title"],
        }
        new_args.update(block_base_args(args))

        return ChildDatabase(**new_args)


@dataclass
class Media(Block):

    caption: ClassVar[TextDescriptor] = TextDescriptor("rich_caption")

    media: Optional[File] = None
    rich_caption: list[RichText] = field(default_factory=list)
    media_type: MediaTypes = MediaTypes.FILE

    def __post_init__(self):
        super().__post_init__()
        self._block_type = BlockTypes.MEDIA

    @classmethod
    def from_dict(cls: Type[Block], args: dict[str, Any]) -> Block:

        media_type = args["type"]
        media = args[media_type]
        if caption := media.get("caption", []):
            caption = rich_text_list(caption)

        new_args: dict[str, Any] = {
            "media": File.from_dict(media),
            "rich_caption": caption,
            "media_type": MediaTypes[media_type.upper()],
        }
        new_args.update(block_base_args(args))

        return Media(**new_args)


@dataclass
class Embed(Block):

    url: Optional[str] = None

    def __post_init__(self):
        super().__post_init__()
        self._block_type = BlockTypes.EMBED

    @classmethod
    def from_dict(cls: Type[Embed], args: dict[str, Any]) -> Embed:

        new_args: dict[str, Any] = {
            "url": args[BlockTypes.EMBED.value]["url"],
        }
        new_args.update(block_base_args(args))

        return Embed(**new_args)


@dataclass
class Bookmark(Block):

    url: Optional[str] = None

    def __post_init__(self):
        super().__post_init__()
        self._block_type = BlockTypes.BOOKMARK

    @classmethod
    def from_dict(cls: Type[Bookmark], args: dict[str, Any]) -> Bookmark:

        new_args: dict[str, Any] = {
            "url": args[BlockTypes.BOOKMARK.value]["url"],
        }
        new_args.update(block_base_args(args))

        return Bookmark(**new_args)


_BLOCK_REVERSE_MAP: dict[BlockTypes, Type[Block]] = {
    BlockTypes.PARAGRAPH: Paragraph,
    BlockTypes.HEADING: Heading,
    BlockTypes.CALLOUT: Callout,
    BlockTypes.QUOTE: Quote,
    BlockTypes.LIST: List,
    BlockTypes.TO_DO: Todo,
    BlockTypes.TOGGLE: Toggle,
    BlockTypes.CODE: Code,
    BlockTypes.CHILD_DATABASE: ChildDatabase,
    BlockTypes.CHILD_PAGE: ChildPage,
    BlockTypes.MEDIA: Media,
    BlockTypes.EMBED: Embed,
    BlockTypes.BOOKMARK: Bookmark,
    BlockTypes.UNSUPPORTED: Block,
}
