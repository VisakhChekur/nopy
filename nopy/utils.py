import logging
from datetime import datetime
from logging import getLogger
from typing import Any
from typing import Callable
from typing import Generator
from typing import Optional
from typing import TypeVar
from typing import Union

from nopy.objects.user import User
from nopy.props.common import Emoji
from nopy.props.common import File
from nopy.props.common import Parent
from nopy.props.common import RichText
from nopy.props.common import Text

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
    data: Optional[dict[str, Any]] = None,
    page_size: int = 100,
    max_pages: int = 0,
    **kwargs: Any,
) -> Generator[T, None, None]:
    """Handles calls that require pagination to get the full results.

    All keyword arguments that are not explicitly expressed in the signature
    are passed to the `api_call` callable. Furthermore, the first argument the
    `api_call` callable takes must be a dictionary that is the `data` argument.
    """

    pages = 0
    if max_pages and max_pages < page_size:
        page_size = max_pages
    if not data:
        data = {"page_size": page_size}

    while True:

        results = api_call(data, **kwargs)

        for res in results["results"]:
            yield map_func(res)
            pages += 1
            # Early exit if specified.
            if max_pages and pages > max_pages:
                return

        if not results["has_more"]:
            break
        data["start_cursor"] = results["next_cursor"]


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
