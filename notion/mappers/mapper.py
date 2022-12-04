from typing import Any, TYPE_CHECKING, Optional

import abc

if TYPE_CHECKING:
    from notion.client import NotionClient

class Mapper(metaclass=abc.ABCMeta):
    """Abstract base class for mappers."""

    def __init__(self, object_dict: Optional[dict[str, Any]]=None, client: Optional["NotionClient"]=None):

        self._obj = object_dict or {}
        self._client = client
    
    @abc.abstractmethod
    def map(self):
        """Maps the given dictionary to the corresponding Notion object."""