from datetime import datetime
from typing import TYPE_CHECKING
from typing import Any
from typing import Optional
from typing import Type
from typing import Union

from nopy.enums import Colors

from .objects.properties import Properties
from .properties.common_properties import Emoji
from .properties.common_properties import File
from .properties.common_properties import Text
from .properties.db_properties import DBProp
from .reverse_maps import PARENT_REVERSE_MAP
from .typings import DBProps
from .typings import PageProps
from .typings import Parents

if TYPE_CHECKING:
    from .client import NotionClient
    from .objects.db import Database

# ----- CONSTANTS -----

# This just helps with intellisense
TYPE = "type"


def block_base_args(
    block: dict[str, Any], client: Optional["NotionClient"] = None
) -> dict[str, Any]:

    base_args = get_base_args(block, client)
    base_args["has_children"] = block["has_children"]

    block_type = block["type"]
    color: Optional[None] = block[block_type].get("color", None)
    if color:
        base_args["color"] = _get_color(color)
    return base_args


def _get_color(color: str) -> Colors:

    return Colors[color.upper()]


def get_base_args(
    obj: dict[str, Any], client: Optional["NotionClient"] = None
) -> dict[str, Any]:
    """Takes the object dictionary and finds all the values that are
    present in all Notion objects (database, page, blocks) and converts them
    into the corresponding type."""

    created_time = datetime.fromisoformat(obj["created_time"])
    last_edited_time = datetime.fromisoformat(obj["last_edited_time"])

    return {
        "id": obj["id"],
        "parent": _get_parent(obj["parent"]),
        "archived": obj["archived"],
        "created_time": created_time,
        "last_edited_time": last_edited_time,
        "client": client,
    }


def _get_parent(parent_dict: dict[str, Any]) -> Parents:

    parent_type = parent_dict.pop(TYPE)
    parent_class = PARENT_REVERSE_MAP[parent_type]
    return parent_class(parent_dict[parent_type])


def get_rich_text_list(rich_text_list: list[dict[str, Any]]) -> list[Text]:

    if not rich_text_list:
        return []
    return [Text.from_dict(rt) for rt in rich_text_list]


def get_icon(icon_dict: dict[str, Any]) -> Optional[Union[File, Emoji]]:

    if not icon_dict:
        return None

    if icon_dict[TYPE] == "emoji":
        return Emoji.from_dict(icon_dict)
    return File.from_dict(icon_dict)


def get_cover(cover_dict: Optional[dict[str, Any]]) -> Optional[File]:

    if not cover_dict:
        return None

    return File.from_dict(cover_dict)


def get_props(
    props_dict: dict[str, Any],
    prop_map: Union[dict[str, Type[DBProps]], dict[str, Type[PageProps]]],
    db: Optional["Database"] = None,
) -> Properties:

    props = Properties()
    for prop in props_dict.values():

        prop_class = prop_map.get(prop[TYPE], DBProp)
        prop_instance = prop_class.from_dict(prop)

        # Finding name if possible.
        # This is needed because the Notion API does not return
        # the name of preperty when retrieving a page.
        # This only applies to pages with databases as the parent
        # and NOT databases as well as pages with other pages as the
        # parent.
        if db:
            prop_instance.name = db.properties._ids[prop_instance.id].name  # type: ignore
        props.add(prop_instance)

    return props
