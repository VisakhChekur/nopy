from dataclasses import InitVar
from datetime import datetime
from typing import TYPE_CHECKING
from typing import Iterable
from typing import Optional
from typing import Union

from pydantic import AnyHttpUrl
from pydantic import Field
from pydantic.dataclasses import dataclass

from notion.helpers import get_plain_text
from notion.properties.common_properties import Emoji
from notion.properties.common_properties import File
from notion.properties.common_properties import Text
from notion.properties.properties import Properties
from notion.typings import Parents

if TYPE_CHECKING:
    from notion.client import NotionClient


@dataclass
class Database:

    db_title: InitVar[Optional[Iterable[Text]]] = None
    plain_title: str = ""
    properties: Properties = Field(default_factory=Properties)
    created_time: Optional[datetime] = None
    last_edited_time: Optional[datetime] = None
    db_description: InitVar[Optional[Iterable[Text]]] = None
    plain_description: str = ""
    icon: Optional[Union[File, Emoji]] = None
    cover: Optional[File] = None
    parent: Optional[Parents] = None
    url: Optional[AnyHttpUrl] = None
    archived: bool = False
    is_inline: bool = False
    _client: Optional["NotionClient"] = None

    def __post_init_post_parse__(
        self,
        db_title: Optional[Iterable[Text]],
        db_description: Optional[Iterable[Text]],
    ):

        if not db_title:
            self.title = [Text(plain_text=self.plain_title)]
        else:
            self.title = db_title
            self.plain_title = get_plain_text(db_title)

        if not db_description:
            self.description = [Text(plain_text=self.plain_description)]
        else:
            self.description = db_description
            self.plain_description = get_plain_text(db_description)

        # Keep track of the original properties if present so they can
        # be used later to determine whether to use the ID or the name
        # when serializing the properties.
        self._og_props = self.properties._ids  # type: ignore
