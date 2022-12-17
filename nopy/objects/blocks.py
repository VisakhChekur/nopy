"""All the block objects avaiable in Notion."""
from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import TYPE_CHECKING
from typing import Any
from typing import ClassVar
from typing import Optional
from typing import Type
from typing import Union

from nopy.enums import Colors
from nopy.enums import HeadingLevels
from nopy.helpers import TextDescriptor
from nopy.objects.block_types import BlockTypes
from nopy.properties.common_properties import Emoji
from nopy.properties.common_properties import File
from nopy.properties.common_properties import Text

from .. import mappers as mp
from .notion_object import NotionObject

if TYPE_CHECKING:
    from ..client import NotionClient


@dataclass
class Block(NotionObject):

    has_children: bool = False

    def __post_init__(self, client: Optional["NotionClient"]):

        self._type: BlockTypes = BlockTypes.UNSUPPORTED

        return super().__post_init__(client)

    @property
    def type(self) -> BlockTypes:
        return self._type

    @classmethod
    def from_dict(
        cls: Type[Block], args: dict[str, Any], client: Optional["NotionClient"] = None
    ) -> Block:
        raise NotImplementedError()


@dataclass
class Paragraph(Block):

    paragraph: ClassVar[TextDescriptor] = TextDescriptor("rich_paragraph")

    rich_paragraph: list[Text] = field(default_factory=list)
    color: Colors = Colors.DEFAULT

    def __post_init__(self, client: Optional["NotionClient"]):

        super().__post_init__(client)
        self._type = BlockTypes.PARAGRAPH

    @classmethod
    def from_dict(
        cls: Type[Block], args: dict[str, Any], client: Optional["NotionClient"] = None
    ) -> Block:

        block_type = BlockTypes.PARAGRAPH.value
        para_args: dict[str, Any] = {
            "rich_paragraph": mp.get_rich_text_list(args[block_type]["rich_text"]),
        }
        para_args.update(mp.block_base_args(args, client))

        return Paragraph(**para_args)


@dataclass
class Heading(Block):
    """The base class for all headings."""

    heading: ClassVar[TextDescriptor] = TextDescriptor("rich_heading")

    rich_heading: list[Text] = field(default_factory=list)
    color: Colors = Colors.DEFAULT
    is_toggleable: bool = False
    heading_level: HeadingLevels = HeadingLevels.HEADING_1

    def __post_init__(self, client: Optional["NotionClient"]):

        super().__post_init__(client)
        self._type = BlockTypes.HEADING

    @classmethod
    def from_dict(
        cls: Type[Heading],
        args: dict[str, Any],
        client: Optional["NotionClient"] = None,
    ) -> Heading:

        base_args: dict[str, Any] = mp.block_base_args(args, client)
        heading_type = args["type"]
        heading_details = args[heading_type]
        heading_args: dict[str, Any] = {
            "rich_heading": mp.get_rich_text_list(heading_details["rich_text"]),
            "is_toggleable": heading_details["is_toggleable"],
            "heading_level": HeadingLevels[heading_type.upper()],
        }
        heading_args.update(base_args)

        return Heading(**heading_args)


@dataclass
class Callout(Block):

    callout: ClassVar[TextDescriptor] = TextDescriptor("rich_callout")

    rich_callout: list[Text] = field(default_factory=list)
    icon: Optional[Union[File, Emoji]] = None
    color: Colors = Colors.DEFAULT

    def __post_init__(self, client: Optional["NotionClient"]):

        super().__post_init__(client)
        self._type = BlockTypes.CALLOUT

    @classmethod
    def from_dict(
        cls: Type[Callout],
        args: dict[str, Any],
        client: Optional["NotionClient"] = None,
    ) -> Callout:

        callout_details = args[BlockTypes.CALLOUT.value]
        callout_args: dict[str, Any] = {
            "rich_callout": mp.get_rich_text_list(callout_details["rich_text"]),
            "icon": mp.get_icon(callout_details["icon"]),
        }
        callout_args.update(mp.block_base_args(args, client))

        return Callout(**callout_args)


@dataclass
class Quote(Block):

    quote: ClassVar[TextDescriptor] = TextDescriptor("rich_quote")

    rich_quote: list[Text] = field(default_factory=list)
    color: Colors = Colors.DEFAULT

    def __post_init__(self, client: Optional["NotionClient"]):

        super().__post_init__(client)
        self._type = BlockTypes.QUOTE

    @classmethod
    def from_dict(
        cls: Type[Quote], args: dict[str, Any], client: Optional["NotionClient"] = None
    ) -> Quote:

        block_type = BlockTypes.QUOTE.value
        quote_args: dict[str, Any] = {
            "rich_quote": mp.get_rich_text_list(args[block_type]["rich_text"])
        }
        quote_args.update(mp.block_base_args(args, client))

        return Quote(**quote_args)


@dataclass
class BulletList(Block):

    item: ClassVar[TextDescriptor] = TextDescriptor("rich_item")

    rich_item: list[Text] = field(default_factory=list)
    color: Colors = Colors.DEFAULT

    def __post_init__(self, client: Optional["NotionClient"]):

        super().__post_init__(client)
        self._type = BlockTypes.BULLETED_LIST_ITEM

    @classmethod
    def from_dict(
        cls: Type[BulletList],
        args: dict[str, Any],
        client: Optional["NotionClient"] = None,
    ) -> BulletList:

        block_type = BlockTypes.BULLETED_LIST_ITEM.value
        bullet_args: dict[str, Any] = {
            "rich_item": mp.get_rich_text_list(args[block_type]["rich_text"])
        }
        bullet_args.update(mp.block_base_args(args))

        return BulletList(**bullet_args)


@dataclass
class NumberedList(Block):

    item: ClassVar[TextDescriptor] = TextDescriptor("rich_item")

    rich_item: list[Text] = field(default_factory=list)
    color: Colors = Colors.DEFAULT

    def __post_init__(self, client: Optional["NotionClient"]):

        super().__post_init__(client)
        self._type = BlockTypes.NUMBERED_LIST_ITEM

    @classmethod
    def from_dict(
        cls: Type[NumberedList],
        args: dict[str, Any],
        client: Optional["NotionClient"] = None,
    ) -> NumberedList:

        block_type = BlockTypes.NUMBERED_LIST_ITEM.value
        number_args: dict[str, Any] = {
            "rich_item": mp.get_rich_text_list(args[block_type]["rich_text"])
        }
        number_args.update(mp.block_base_args(args))

        return NumberedList(**number_args)


@dataclass
class Todo(Block):

    item: ClassVar[TextDescriptor] = TextDescriptor("rich_item")

    rich_item: list[Text] = field(default_factory=list)
    checked: bool = False
    color: Colors = Colors.DEFAULT

    def __post_init__(self, client: Optional["NotionClient"]):

        super().__post_init__(client)
        self._type = BlockTypes.TO_DO

    @classmethod
    def from_dict(
        cls: Type[Block], args: dict[str, Any], client: Optional["NotionClient"] = None
    ) -> Block:

        todo_details = args[BlockTypes.TO_DO.value]

        todo_args: dict[str, Any] = {
            "rich_item": mp.get_rich_text_list(todo_details["rich_text"]),
            "checked": todo_details["checked"],
        }
        todo_args.update(mp.block_base_args(args))

        return Todo(**todo_args)


@dataclass
class Toggle(Block):
    def __post_init__(self, client: Optional["NotionClient"]):

        super().__post_init__(client)
        self._type = BlockTypes.TOGGLE

    @classmethod
    def from_dict(
        cls: Type[Toggle], args: dict[str, Any], client: Optional["NotionClient"] = None
    ) -> Toggle:

        toggle_args: dict[str, Any] = {}

        return Toggle(**toggle_args)


@dataclass
class ChildPage(Block):
    def __post_init__(self, client: Optional["NotionClient"]):

        super().__post_init__(client)
        self._type = BlockTypes.CHILD_PAGE

    @classmethod
    def from_dict(
        cls: Type[ChildPage],
        args: dict[str, Any],
        client: Optional["NotionClient"] = None,
    ) -> ChildPage:

        child_page_args: dict[str, Any] = {}

        return ChildPage(**child_page_args)


@dataclass
class ChildDatabase(Block):
    def __post_init__(self, client: Optional["NotionClient"]):

        super().__post_init__(client)
        self._type = BlockTypes.CHILD_DATABASE

    @classmethod
    def from_dict(
        cls: Type[ChildDatabase],
        args: dict[str, Any],
        client: Optional["NotionClient"] = None,
    ) -> ChildDatabase:

        child_database_args: dict[str, Any] = {}

        return ChildDatabase(**child_database_args)


@dataclass
class Embed(Block):
    def __post_init__(self, client: Optional["NotionClient"]):

        super().__post_init__(client)
        self._type = BlockTypes.EMBED

    @classmethod
    def from_dict(
        cls: Type[Embed], args: dict[str, Any], client: Optional["NotionClient"] = None
    ) -> Embed:

        embed_args: dict[str, Any] = {}

        return Embed(**embed_args)


@dataclass
class Image(Block):
    def __post_init__(self, client: Optional["NotionClient"]):

        super().__post_init__(client)
        self._type = BlockTypes.IMAGE

    @classmethod
    def from_dict(
        cls: Type[Image], args: dict[str, Any], client: Optional["NotionClient"] = None
    ) -> Image:

        image_args: dict[str, Any] = {}

        return Image(**image_args)


@dataclass
class Video(Block):
    def __post_init__(self, client: Optional["NotionClient"]):

        super().__post_init__(client)
        self._type = BlockTypes.VIDEO

    @classmethod
    def from_dict(
        cls: Type[Video], args: dict[str, Any], client: Optional["NotionClient"] = None
    ) -> Video:

        video_args: dict[str, Any] = {}

        return Video(**video_args)


@dataclass
class FileBlock(Block):
    def __post_init__(self, client: Optional["NotionClient"]):

        super().__post_init__(client)
        self._type = BlockTypes.FILE

    @classmethod
    def from_dict(
        cls: Type[FileBlock],
        args: dict[str, Any],
        client: Optional["NotionClient"] = None,
    ) -> FileBlock:

        file_args: dict[str, Any] = {}

        return FileBlock(**file_args)


@dataclass
class Pdf(Block):
    def __post_init__(self, client: Optional["NotionClient"]):

        super().__post_init__(client)
        self._type = BlockTypes.PDF

    @classmethod
    def from_dict(
        cls: Type[Pdf], args: dict[str, Any], client: Optional["NotionClient"] = None
    ) -> Pdf:

        pdf_args: dict[str, Any] = {}

        return Pdf(**pdf_args)


@dataclass
class Bookmark(Block):
    def __post_init__(self, client: Optional["NotionClient"]):

        super().__post_init__(client)
        self._type = BlockTypes.BOOKMARK

    @classmethod
    def from_dict(
        cls: Type[Bookmark],
        args: dict[str, Any],
        client: Optional["NotionClient"] = None,
    ) -> Bookmark:

        bookmark_args: dict[str, Any] = {}

        return Bookmark(**bookmark_args)


@dataclass
class Equation(Block):
    def __post_init__(self, client: Optional["NotionClient"]):

        super().__post_init__(client)
        self._type = BlockTypes.EQUATION

    @classmethod
    def from_dict(
        cls: Type[Equation],
        args: dict[str, Any],
        client: Optional["NotionClient"] = None,
    ) -> Equation:

        equation_args: dict[str, Any] = {}

        return Equation(**equation_args)


@dataclass
class Divider(Block):
    def __post_init__(self, client: Optional["NotionClient"]):

        super().__post_init__(client)
        self._type = BlockTypes.DIVIDER

    @classmethod
    def from_dict(
        cls: Type[Divider],
        args: dict[str, Any],
        client: Optional["NotionClient"] = None,
    ) -> Divider:

        divider_args: dict[str, Any] = {}

        return Divider(**divider_args)


@dataclass
class TableOfContents(Block):
    def __post_init__(self, client: Optional["NotionClient"]):

        super().__post_init__(client)
        self._type = BlockTypes.TABLE_OF_CONTENTS

    @classmethod
    def from_dict(
        cls: Type[TableOfContents],
        args: dict[str, Any],
        client: Optional["NotionClient"] = None,
    ) -> TableOfContents:

        table_of_contents_args: dict[str, Any] = {}

        return TableOfContents(**table_of_contents_args)


@dataclass
class Column(Block):
    def __post_init__(self, client: Optional["NotionClient"]):

        super().__post_init__(client)
        self._type = BlockTypes.COLUMN

    @classmethod
    def from_dict(
        cls: Type[Column], args: dict[str, Any], client: Optional["NotionClient"] = None
    ) -> Column:

        column_args: dict[str, Any] = {}

        return Column(**column_args)


@dataclass
class ColumnList(Block):
    def __post_init__(self, client: Optional["NotionClient"]):

        super().__post_init__(client)
        self._type = BlockTypes.COLUMN_LIST

    @classmethod
    def from_dict(
        cls: Type[ColumnList],
        args: dict[str, Any],
        client: Optional["NotionClient"] = None,
    ) -> ColumnList:

        column_list_args: dict[str, Any] = {}

        return ColumnList(**column_list_args)


@dataclass
class LinkPreview(Block):
    def __post_init__(self, client: Optional["NotionClient"]):

        super().__post_init__(client)
        self._type = BlockTypes.LINK_PREVIEW

    @classmethod
    def from_dict(
        cls: Type[LinkPreview],
        args: dict[str, Any],
        client: Optional["NotionClient"] = None,
    ) -> LinkPreview:

        link_preview_args: dict[str, Any] = {}

        return LinkPreview(**link_preview_args)


@dataclass
class SyncedBlock(Block):
    def __post_init__(self, client: Optional["NotionClient"]):

        super().__post_init__(client)
        self._type = BlockTypes.SYNCED_BLOCK

    @classmethod
    def from_dict(
        cls: Type[SyncedBlock],
        args: dict[str, Any],
        client: Optional["NotionClient"] = None,
    ) -> SyncedBlock:

        synced_block_args: dict[str, Any] = {}

        return SyncedBlock(**synced_block_args)


@dataclass
class Template(Block):
    def __post_init__(self, client: Optional["NotionClient"]):

        super().__post_init__(client)
        self._type = BlockTypes.TEMPLATE

    @classmethod
    def from_dict(
        cls: Type[Template],
        args: dict[str, Any],
        client: Optional["NotionClient"] = None,
    ) -> Template:

        template_args: dict[str, Any] = {}

        return Template(**template_args)


@dataclass
class LinkToPage(Block):
    def __post_init__(self, client: Optional["NotionClient"]):

        super().__post_init__(client)
        self._type = BlockTypes.LINK_TO_PAGE

    @classmethod
    def from_dict(
        cls: Type[LinkToPage],
        args: dict[str, Any],
        client: Optional["NotionClient"] = None,
    ) -> LinkToPage:

        link_to_page_args: dict[str, Any] = {}

        return LinkToPage(**link_to_page_args)


@dataclass
class Table(Block):
    def __post_init__(self, client: Optional["NotionClient"]):

        super().__post_init__(client)
        self._type = BlockTypes.TABLE

    @classmethod
    def from_dict(
        cls: Type[Table], args: dict[str, Any], client: Optional["NotionClient"] = None
    ) -> Table:

        table_args: dict[str, Any] = {}

        return Table(**table_args)


@dataclass
class TableRow(Block):
    def __post_init__(self, client: Optional["NotionClient"]):

        super().__post_init__(client)
        self._type = BlockTypes.TABLE_ROW

    @classmethod
    def from_dict(
        cls: Type[TableRow],
        args: dict[str, Any],
        client: Optional["NotionClient"] = None,
    ) -> TableRow:

        table_row_args: dict[str, Any] = {}

        return TableRow(**table_row_args)
