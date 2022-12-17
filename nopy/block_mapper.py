from typing import TYPE_CHECKING
from typing import Any
from typing import Optional

from .objects import blocks
from .reverse_maps import BLOCK_REVERSE_MAP

if TYPE_CHECKING:
    from .client import NotionClient


def map_to_block(
    block: dict[str, Any], client: Optional["NotionClient"] = None
) -> blocks.Block:

    block_type = block["type"]
    try:
        block_class = BLOCK_REVERSE_MAP[block_type]
    except KeyError:
        block_class = BLOCK_REVERSE_MAP["unsupported"]
    return block_class.from_dict(block)
