from typing import Iterable

from notion.properties.common_properties import RichText


def get_plain_text(rich_texts: Iterable[RichText]) -> str:
    """Returns the combined plain text from a list of rich text objects."""

    return " ".join((txt.plain_text for txt in rich_texts))
