from typing import Any, Optional
import abc


from notion.client import NotionClient

class NotionObject(metaclass=abc.ABCMeta):
    """Base class for all Notion objects."""

    def __init__(self, client: Optional[NotionClient]):
        """Constructor for NotionObject.
        
        Args:
            client:
                An instance of NotionClient.
        """
        self._client: Optional[NotionClient] = client

    @abc.abstractmethod
    def serialize(self) -> dict[str, Any]:
        """Serializes the instance to a dictionary following the Notion spec."""

        
    @abc.abstractmethod
    def refresh(self) -> None:
        """Refreshes the instance.
        
        Calls the Notion API to get the latest version of the instance. Changes
        WILL BE LOST if they're not updated with `self.update()`.
        """
    
    @abc.abstractmethod
    def update(self) -> None:
        """Updates the instance to the Notion server.
        
        The Notion object is updated and refreshed. There is no need to call
        `self.refresh()`.
        """