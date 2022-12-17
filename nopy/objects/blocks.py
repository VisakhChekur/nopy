"""All the block objects avaiable in Notion."""
from __future__ import annotations

from dataclasses import InitVar
from dataclasses import dataclass
from dataclasses import field
from typing import TYPE_CHECKING
from typing import Any
from typing import ClassVar
from typing import Optional
from typing import Type
from typing import Union

from nopy.enums import BackgroundColors
from nopy.enums import Colors
from nopy.helpers import TextDescriptor
from nopy.helpers import get_base_args_dict_block
from nopy.objects.block_types import BlockTypes
from nopy.properties.common_properties import Emoji
from nopy.properties.common_properties import File
from nopy.properties.common_properties import Text

from .notion_object import NotionObject

if TYPE_CHECKING:
    from ..client import NotionClient


@dataclass
class Block(NotionObject):

    has_children: bool = False
    client: InitVar[Optional["NotionClient"]]

    def __post_init__(self, client: Optional["NotionClient"]):

        self._type: BlockTypes = BlockTypes.UNSUPPORTED

        return super().__post_init__(client)

    @property
    def type(self) -> BlockTypes:
        return self._type

    @classmethod
    def from_dict(cls: Type[Block], args: dict[str, Any]) -> Block:

        return Block(**get_base_args_dict_block(args))


@dataclass
class Paragraph(Block):

    paragraph: ClassVar[TextDescriptor] = TextDescriptor("rich_paragraph")

    rich_paragraph: list[Text] = field(default_factory=list)
    color: Union[Colors, BackgroundColors] = Colors.DEFAULT

    def __post_init__(self, client: Optional["NotionClient"]):

        self._type = BlockTypes.PARAGRAPH
        return super().__post_init__(client)


@dataclass
class Heading(Block):
    """The base class for all headings."""

    heading: ClassVar[TextDescriptor] = TextDescriptor("rich_heading")

    rich_heading: list[Text] = field(default_factory=list)
    color: Union[Colors, BackgroundColors] = Colors.DEFAULT
    is_toggleable: bool = False

    def __post_init__(self, client: Optional["NotionClient"]):

        self._type = BlockTypes.UNSUPPORTED
        return super().__post_init__(client)


# TODO: Check the returned object if the heading can be toggled
@dataclass
class HeadingOne(Heading):
    def __post_init__(self, client: Optional["NotionClient"]):

        self._type = BlockTypes.HEADING_ONE
        return super().__post_init__(client)


@dataclass
class HeadingTwo(Heading):
    def __post_init__(self, client: Optional["NotionClient"]):

        self._type = BlockTypes.HEADING_ONE
        return super().__post_init__(client)


@dataclass
class HeadingThree(Heading):
    def __post_init__(self, client: Optional["NotionClient"]):

        self._type = BlockTypes.HEADING_ONE
        return super().__post_init__(client)


@dataclass
class Callout(Block):

    callout: ClassVar[TextDescriptor] = TextDescriptor("callout")

    rich_callout: list[Text] = field(default_factory=list)
    icon: Optional[Union[File, Emoji]] = None
    color: Union[Colors, BackgroundColors] = Colors.DEFAULT
    children: list[Block] = field(default_factory=list)

    def __post_init__(self, client: Optional["NotionClient"]):

        self._type = BlockTypes.CALLOUT
        return super().__post_init__(client)


@dataclass
class Quote(Block):

    quote: ClassVar[TextDescriptor] = TextDescriptor("rich_quote")

    rich_quote: list[Text] = field(default_factory=list)
    color: Union[Colors, BackgroundColors] = Colors.DEFAULT
