import abc
from typing import TYPE_CHECKING, Any, Optional
from dataclasses import InitVar

from pydantic.dataclasses import dataclass

if TYPE_CHECKING:
    from notion.client import NotionClient

class Config:

    underscore_attrs_are_private = True


@dataclass(config=Config)
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
    def refresh(self, in_place:bool=True):
        """Refreshes the instance with the latest version in the Notion 
        server."""