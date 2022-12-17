from typing import Any
from typing import Iterable

from .properties.common_properties import RichText
from .properties.common_properties import Text


def get_plain_text(rich_texts: Iterable[RichText]) -> str:
    """Returns the combined plain text from a list of rich text objects."""

    return " ".join((txt.plain_text for txt in rich_texts))


def serialize_text_list(text: list[Text]) -> list[dict[str, Any]]:

    # If the space is not added here, then no space shows up in the database
    # name as well
    serialized: list[dict[str, Any]] = [t.serialize() for t in text]
    for t in serialized[:-1]:
        t["text"]["content"] += " "
    return serialized


class TextDescriptor:
    """Implementation of the descriptor protocol to handle attributes
    of classes that deal with arrays `Text` instances."""

    def __init__(self, storage_name: str):

        self.storage_name = storage_name

    def __get__(self, instance: object, _):

        return get_plain_text(instance.__dict__[self.storage_name])

    def __set__(self, instance: object, value: str):

        instance.__dict__[self.storage_name] = [Text(value)]
