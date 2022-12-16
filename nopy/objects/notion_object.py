from dataclasses import KW_ONLY
from dataclasses import InitVar
from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING
from typing import Optional

from ..typings import Parents

if TYPE_CHECKING:
    from nopy.client import NotionClient


@dataclass
class NotionObject:
    """The base class from which all other Notion objects inherit."""

    _: KW_ONLY
    id: str = ""
    parent: Optional[Parents] = None
    archived: bool = False
    created_time: Optional[datetime] = None
    last_edited_time: Optional[datetime] = None
    client: InitVar[Optional["NotionClient"]] = None

    def __post_init__(self, client: Optional["NotionClient"]):
        self._client = client

    # @abc.abstractmethod
    # def serialize(self, create: bool=False) -> dict[str, Any]:
    #     """Serializes the instance according to the Notion spec."""

    def update(self) -> None:
        """Updates the instance to the Notion server."""
        raise NotImplementedError("to be implemented by subclass")

    def refresh(self, in_place: bool = True) -> "NotionObject":
        """Refreshes the instance with the latest version in the Notion
        server."""
        raise NotImplementedError("to be implemented by subclass")
