import logging
from datetime import datetime
from logging import getLogger
from typing import TYPE_CHECKING
from typing import Any
from typing import Callable
from typing import Generator
from typing import Optional
from typing import TypeVar
from typing import Union

from nopy.constants import DB_PROPS_REVERSE_MAP
from nopy.objects.user import User
from nopy.properties import Properties
from nopy.props.base import ObjectProperty
from nopy.props.common import Emoji
from nopy.props.common import File
from nopy.props.common import Parent
from nopy.props.common import RichText
from nopy.props.common import Text

if TYPE_CHECKING:
    from nopy.client import NotionClient


# ----- TYPES ------
API_CALL = Callable[..., dict[str, Any]]
T = TypeVar("T")


def make_logger(log_level: int) -> logging.Logger:

    logger = getLogger(__package__)
    logger.setLevel(log_level)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(logging.BASIC_FORMAT)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


class TextDescriptor:
    """Implementation of the descriptor protocol to handle attributes
    of classes that deal with arrays of `Text` properties."""

    def __init__(self, storage_name: str):

        # storage_name is the name of the attribute within
        # the class that holds the array which is to be used
        # when finding the plain text or vice versa
        self.storage_name = storage_name

    def __get__(self, instance: object, _):
        """Gets the combined plain text from a list of rich text."""

        rich_text: list[RichText] = instance.__dict__[self.storage_name]
        return " ".join(rt.plain_text for rt in rich_text)

    def __set__(self, instance: object, value: str):

        msg = f"value must be a string, use '{self.storage_name}' for adding text with style information"
        assert isinstance(value, str), msg

        instance.__dict__[self.storage_name] = [Text(value)]


def paginate(
    api_call: API_CALL,
    map_func: Callable[..., T],
    max_pages: int = 0,
    map_args: Optional[dict[str, Any]] = None,
    client: Optional["NotionClient"] = None,
    **kwargs: Any,
) -> Generator[T, None, None]:
    """Handles calls that require pagination to get the full results.

    All keyword arguments that are not explicitly expressed in the signature
    are passed to the `api_call` callable.

    All `map_args` are passed to the `map_func` when calling it along with the
    result. The result is the first argument that's passed in.
    """

    pages = 0
    next_cursor = None
    map_args = map_args or {}

    while True:

        results = api_call(**kwargs, start_cursor=next_cursor)

        for res in results["results"]:
            notion_obj = map_func(res, **map_args)
            if hasattr(notion_obj, "set_client"):
                notion_obj.set_client(client)  # type: ignore
            yield notion_obj
            pages += 1
            # Early exit if specified.
            if max_pages and pages > max_pages:
                return

        if not results["has_more"]:
            return
        next_cursor = results["next_cursor"]


# ----- Mapping Utilities -----


def base_obj_args(args: dict[str, Any]) -> dict[str, Any]:
    """Parses the common arguments found in all Notion objects
    and converts them to the required data type."""

    new_args: dict[str, Any] = {
        "id": args["id"],
        "archived": args["archived"],
    }

    # Getting the parent
    if parent := args.get("parent", None):
        new_args["parent"] = Parent.from_dict(parent)

    # Getting users
    for key in ("created_by", "last_edited_by"):
        if value := args.get(key, None):
            new_args[key] = User.from_dict(value)

    # Getting time
    for key in ("created_time", "last_edited_time"):
        if value := args.get(key, None):
            new_args[key] = datetime.fromisoformat(value)

    return new_args


def rich_text_list(rich_texts: list[dict[str, Any]]) -> list[RichText]:
    """Parses the list of dictionaries into a list of RichText objects."""

    return [RichText.from_dict(rt) for rt in rich_texts]


def get_icon(icon: Optional[dict[str, Any]]) -> Optional[Union[File, Emoji]]:

    if not icon:
        return None

    icon_type = icon["type"]

    if icon_type == "emoji":
        return Emoji.from_dict(icon)
    return File.from_dict(icon)


def get_cover(cover: Optional[dict[str, Any]]) -> Optional[File]:

    if not cover:
        return None
    return File.from_dict(cover)


def base_db_prop_args(args: dict[str, Any]):

    return {
        "id": args["id"],
        "name": args["name"],
    }


def get_props(props: dict[str, Any]) -> Properties:

    properties = Properties()
    for prop in props.values():

        prop_type = prop["type"]
        if prop_type == "title":
            continue

        prop_class = DB_PROPS_REVERSE_MAP.get(prop_type, ObjectProperty)
        prop_instance = prop_class.from_dict(prop)
        properties.add(prop_instance)

    return properties
