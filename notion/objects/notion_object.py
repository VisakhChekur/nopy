import abc
from dataclasses import InitVar
from typing import TYPE_CHECKING
from typing import Any
from typing import Optional

if TYPE_CHECKING:
    from notion.client import NotionClient


class NotionObject(metaclass=abc.ABCMeta):

    client: InitVar[Optional["NotionClient"]] = None

    def __post_init_parse__(self, client: Optional["NotionClient"]):
        self._client = client

    @abc.abstractmethod
    def serialize(self) -> dict[str, Any]:
        """Serializes the instance according to the Notion spec."""

    @abc.abstractmethod
    def update(self):
        """Updates the instance to the Notion server and refreshes."""

    @abc.abstractmethod
    def refresh(self, in_place: bool = True):
        """Refreshes the instance with the latest version in the Notion
        server."""
