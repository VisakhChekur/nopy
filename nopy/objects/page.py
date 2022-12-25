from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import TYPE_CHECKING
from typing import Any
from typing import ClassVar
from typing import Optional
from typing import Type
from typing import Union

import nopy.props.page_props as pgp
from nopy.enums import ObjectTypes
from nopy.errors import NoClientFoundError
from nopy.objects.notion_object import NotionObject
from nopy.properties import Properties
from nopy.props.base import ObjectProperty
from nopy.props.common import Emoji
from nopy.props.common import File
from nopy.props.common import RichText
from nopy.types import PageProps
from nopy.utils import TextDescriptor
from nopy.utils import base_obj_args
from nopy.utils import get_cover
from nopy.utils import get_icon
from nopy.utils import rich_text_list

if TYPE_CHECKING:
    pass


@dataclass
class Page(NotionObject):
    """A representation of a page in Notion.

    Attributes:
        title (str): The title of the datbase without styling.

        rich_title: The title of the page with style information.

        properties: The properties of the page.

        icon: The icon of the page, if any.

        cover: The cover of the page, if any.

        url: The URL of the page, if any.

        archived (bool): Denotes whether the page is archived or not.

        id (str): The id of the page.

        parent (Parent): The parent of the page.

        created_time (Optional[datetime]):
            The time the page was created.

        last_edited_time (Optional[datetime]):
            The time the page was last edited.

        type (ObjectTypes):
            The type of the Notion object which will always be
            `ObjectTypes.PAGE`.

    """

    _REVERSE_MAP: ClassVar[dict[str, Type["PageProps"]]] = {
        "checkbox": pgp.PCheckbox,
        "created_time": pgp.PCreatedTime,
        "created_by": pgp.PCreatedby,
        "date": pgp.PDate,
        "email": pgp.PEmail,
        "files": pgp.PFiles,
        "formula": pgp.PFormula,
        "last_edited_by": pgp.PLastEditedBy,
        "last_edited_time": pgp.PLastEditedTime,
        "multi_select": pgp.PMultiselect,
        "number": pgp.PNumber,
        "people": pgp.PPeople,
        "phone_number": pgp.PPhonenumber,
        "relation": pgp.PRelation,
        "rich_text": pgp.PRichtext,
        "rollup": pgp.PRollup,
        "select": pgp.PSelect,
        "status": pgp.PStatus,
        "url": pgp.PUrl,
    }
    title: ClassVar[TextDescriptor] = TextDescriptor("rich_title")

    rich_title: list[RichText] = field(default_factory=list)
    properties: Properties = field(default_factory=Properties)
    icon: Optional[Union[File, Emoji]] = None
    cover: Optional[File] = None
    is_inline: bool = False
    url: str = ""

    def __post_init__(self):

        super().__post_init__()
        self._type = ObjectTypes.PAGE
        self._og_props = set(self.properties._ids.keys())  # type: ignore

    def update(self, in_place: bool = False) -> Page:
        """Updates the page.

        Attributes:
            in_place (bool):
                If `True`, then this instance is updated in place.

        Returns:
            The updated Page instance. Returns `self` if `in_place` is
                `True`.
        """

        if not self._client:
            raise NoClientFoundError("no client is associated with this instance")

        page = self.serialize()
        # Parent should not be present when updating
        page.pop("parent")

        updated_page = self._client.update_page(self.id, page)

        if not in_place:
            return updated_page
        self.__dict__.clear()
        self.__dict__ = updated_page.__dict__
        return self

    def serialize(self) -> dict[str, Any]:

        serialized: dict[str, Any] = {
            "archived": self.archived,
            "properties": self.properties.serialize(),
        }

        for attr in ("parent", "icon", "cover"):
            value = self.__dict__.get(attr, None)
            serialized[attr] = value if value is None else value.serialize()

        serialized["properties"]["title"] = {
            "title": [rt.serialize() for rt in self.rich_title]
        }

        return serialized

    @classmethod
    def from_dict(cls: Type[Page], args: dict[str, Any]) -> Page:

        # This is needed because a Page object returned by Notion
        # doesn't have the page title directly accessible like in a
        # Database. The title has to be accessed from the `properties`.
        # Also if the page is part of a database, then the keys of the
        # properties are not the ids, but rather the name of the property.
        props = args["properties"].values()
        title_gen = (prop for prop in props if prop["id"] == "title")
        title_list: list[dict[str, Any]] = next(title_gen)["title"]

        new_args: dict[str, Any] = {
            "rich_title": rich_text_list(title_list),
            "icon": get_icon(args["icon"]),
            "cover": get_cover(args["cover"]),
            "url": args["url"],
        }
        # Getting the database properties
        properties = Properties()
        for name, prop in args["properties"].items():

            prop_type = prop["type"]
            if prop_type == "title":
                continue

            prop_class = cls._REVERSE_MAP.get(prop_type, ObjectProperty)
            prop["name"] = name
            prop_instance = prop_class.from_dict(prop)
            properties.add(prop_instance)

        new_args["properties"] = properties
        new_args.update(base_obj_args(args))

        return Page(**new_args)
