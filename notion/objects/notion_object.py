import abc
from dataclasses import InitVar
from typing import TYPE_CHECKING
from typing import Optional

if TYPE_CHECKING:
    from notion.client import NotionClient


class NotionObject(metaclass=abc.ABCMeta):
    """The base class from which all other Notion objects inherit."""

    client: InitVar[Optional["NotionClient"]] = None

    def __post_init__(self, client: Optional["NotionClient"]):
        self._client = client

    # @abc.abstractmethod
    # def serialize(self, create: bool=False) -> dict[str, Any]:
    #     """Serializes the instance according to the Notion spec."""

    @abc.abstractmethod
    def update(self):
        """Updates the instance to the Notion server."""

    @abc.abstractmethod
    def refresh(self, in_place: bool = True) -> "NotionObject":
        """Refreshes the instance with the latest version in the Notion
        server."""
