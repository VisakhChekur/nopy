from copy import deepcopy
from datetime import datetime
from typing import TYPE_CHECKING
from typing import Any
from typing import Optional
from typing import Type
from typing import Union
from typing import cast

from .objects.db import Database
from .objects.page import Page
from .objects.properties import Properties
from .properties.common_properties import Emoji
from .properties.common_properties import File
from .properties.common_properties import Text
from .properties.db_properties import DBProp
from .properties.page_properties import PTitle
from .reverse_maps import DB_PROPS_REVERSE_MAP
from .reverse_maps import PAGE_PROPS_REVERSE_MAP
from .reverse_maps import PARENT_REVERSE_MAP
from .typings import DBProps
from .typings import PageProps
from .typings import Parents

if TYPE_CHECKING:
    from .client import NotionClient

# ----- CONSTANTS -----

# This just helps with intellisense
TYPE = "type"


def map_to_db(
    db: dict[str, Any], client: "NotionClient", no_mutate: bool = False
) -> Database:
    """Maps the given database to a Database instance.

    The dictionary MUST adhere to the Notion specifications.
    """

    if no_mutate:
        db = deepcopy(db)

    db_args = {
        "rich_title": _get_rich_text_list(db["title"]),
        "rich_description": _get_rich_text_list(db["description"]),
        "icon": _get_icon(db["icon"]),
        "cover": _get_cover(db["cover"]),
        "url": db["url"],
        "is_inline": db["is_inline"],
        "properties": _get_props(db["properties"], DB_PROPS_REVERSE_MAP),
        "client": client,
    }
    db_args.update(_get_base_args(db))

    return Database(**db_args)


def map_to_page(
    page: dict[str, Any],
    db: Optional[Database],
    client: "NotionClient",
    no_mutate: bool = False,
) -> Page:
    """Maps the given dictionary to a Page instance.

    The dictionary MUST adhere to the Notion specifications.
    """

    if no_mutate:
        page = deepcopy(page)

    properties = _get_props(page["properties"], PAGE_PROPS_REVERSE_MAP, db)
    # `title` is not directly provided as in the case of databases
    # which means it has to be found from the properties of the page
    title = cast(PTitle, properties["title"])

    page_args = {
        "properties": properties,
        "icon": _get_icon(page["icon"]),
        "cover": _get_cover(page["cover"]),
        "url": page["url"],
        "rich_title": title.rich_title,
        "client": client,
    }
    page_args.update(_get_base_args(page))

    return Page(**page_args)


def _get_base_args(obj: dict[str, Any]) -> dict[str, Any]:
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
    }


def _get_parent(parent_dict: dict[str, Any]) -> Parents:

    parent_type = parent_dict.pop(TYPE)
    parent_class = PARENT_REVERSE_MAP[parent_type]
    return parent_class(parent_dict[parent_type])


def _get_rich_text_list(rich_text_list: list[dict[str, Any]]) -> list[Text]:

    if not rich_text_list:
        return []
    return [Text.from_dict(rt) for rt in rich_text_list]


def _get_icon(icon_dict: dict[str, Any]) -> Optional[Union[File, Emoji]]:

    if not icon_dict:
        return None

    if icon_dict[TYPE] == "emoji":
        return Emoji.from_dict(icon_dict)
    return File.from_dict(icon_dict)


def _get_cover(cover_dict: Optional[dict[str, Any]]) -> Optional[File]:

    if not cover_dict:
        return None

    return File.from_dict(cover_dict)


def _get_props(
    props_dict: dict[str, Any],
    prop_map: Union[dict[str, Type[DBProps]], dict[str, Type[PageProps]]],
    db: Optional[Database] = None,
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
