from copy import deepcopy
from typing import TYPE_CHECKING
from typing import Any
from typing import Optional
from typing import Union
from typing import cast

import dateutil.parser as date_parser

from .objects.db import Database
from .objects.page import Page
from .objects.properties import Properties
from .properties import common_properties as cp
from .properties import db_properties as dbp
from .properties import page_properties as pgp
from .typings import DBProps
from .typings import PageProps
from .typings import Parents

if TYPE_CHECKING:
    from notion.client import NotionClient

DB_PROPS_REVERSE_MAP: dict[str, type[DBProps]] = {
    "title": dbp.DBTitle,
    "rich_text": dbp.DBText,
    "number": dbp.DBNumber,
    "select": dbp.DBSelect,
    "multi_select": dbp.DBMultiSelect,
    "date": dbp.DBDate,
    "files": dbp.DBFiles,
    "checkbox": dbp.DBCheckbox,
    "url": dbp.DBUrl,
    "email": dbp.DBEmail,
    "phone_number": dbp.DBPhoneNumber,
    "formula": dbp.DBFormula,
    "created_time": dbp.DBCreatedTime,
    "created_by": dbp.DBCreatedBy,
    "last_edited_time": dbp.DBLastEditedTime,
    "last_edited_by": dbp.DBLastEditedBy,
    "status": dbp.DBStatus,
    "unsupported": dbp.DBProp,
}

PAGE_PROPS_REVERSE_MAP: dict[str, type[PageProps]] = {
    "unsupported": pgp.PProp,
    "title": pgp.PTitle,
    "rich_text": pgp.PText,
    "number": pgp.PNumber,
    "select": pgp.PSelect,
    "multi_select": pgp.PMultiSelect,
    "date": pgp.PDate,
    "formula": pgp.PFormula,
    "files": pgp.PFile,
    "checkbox": pgp.PCheckbox,
    "url": pgp.PUrl,
    "email": pgp.PEmail,
    "phone_number": pgp.PPhoneNumber,
    "created_time": pgp.PCreatedTime,
    "last_edited_time": pgp.PLastEditedTime,
}

PARENT_REVERSE_MAP: dict[str, type[Parents]] = {
    "database_id": cp.DatabaseParent,
    "page_id": cp.PageParent,
    "block_id": cp.BlockParent,
    "workspace": cp.WorkspaceParent,
}


class Mapper:
    """Handles mapping response from the Notion API to the correspoding
    object."""

    # Also includes unsupported keys as well.
    UNNECESSARY_KEYS = (
        "object",
        "created_by",
        "last_edited_by",
        "title",
        "description",
    )

    def __init__(self, client: Optional["NotionClient"] = None):

        self._client = client

    def map_to_db(self, db: dict[str, Any], *, no_mutate: bool = False) -> Database:
        """Maps the given dictionary to a `Database`.

        Args:
            db: The dictionary of containing the data of the database in a
                format as in the Notion specifications.

            no_mutate: If 'True', a deepcopy is performed on the given `db`.

        Returns:
            An instance of `Database`.
        """
        if no_mutate:
            db = deepcopy(db)

        db["cover"] = self._get_cover(db["cover"])
        db["created_time"] = date_parser.parse(db["created_time"])
        db["last_edited_time"] = date_parser.parse(db["last_edited_time"])
        db["rich_title"] = [cp.Text.from_dict(t) for t in db["title"]]
        db["rich_description"] = [cp.Text.from_dict(t) for t in db["description"]]
        db["icon"] = self._get_icon(db["icon"])
        db["properties"] = self._get_db_props(db["properties"])
        db["client"] = self._client
        db["id"] = db["id"].replace("-", "")

        # Getting parent
        db["parent"] = self._get_parent(db["parent"])

        # Removing unsupported/unnecessary keys
        for key in Mapper.UNNECESSARY_KEYS:
            db.pop(key, None)

        return Database(**db)

    def map_to_page(
        self,
        page: dict[str, Any],
        db: Optional[Database] = None,
        *,
        no_mutate: bool = True
    ) -> Page:
        """Maps the given dictionary to a `Page`.

        Args:
            page: The dictionary of containing the data of the page in a
                  format as in the Notion specifications.

            db: This should be the database within which the `Page` lies. If
                provided, it is used to try to find the name of the property
                using the `id` of the property.

            no_mutate: If 'True', a deepcopy is performed on the given `page`.

        Returns:
            An instance of `Page`.
        """

        if no_mutate:
            page = deepcopy(page)

        page["cover"] = self._get_cover(page["cover"])
        page["created_time"] = date_parser.parse(page["created_time"])
        page["last_edited_time"] = date_parser.parse(page["last_edited_time"])
        page["icon"] = self._get_icon(page["icon"])
        page["client"] = self._client
        page["id"] = page["id"].replace("-", "")
        page["properties"] = self._get_page_props(page["properties"], db)

        # Getting parent
        page["parent"] = self._get_parent(page["parent"])

        # There's no 'title' property like in a database
        title = cast(pgp.PTitle, page["properties"]["title"])
        page["rich_title"] = title.rich_title

        for key in Mapper.UNNECESSARY_KEYS:
            page.pop(key, None)

        return Page(**page)

    def _get_parent(self, parent_dict: dict[str, Any]) -> Parents:

        parent_type = parent_dict["type"]
        parent_class = PARENT_REVERSE_MAP[parent_type]
        return parent_class(parent_dict[parent_type])

    def _get_cover(self, cover_dict: Optional[dict[str, Any]]) -> Optional[cp.File]:

        if not cover_dict:
            return None
        return cp.File.from_dict(cover_dict)

    def _get_icon(
        self, icon_dict: dict[str, Any]
    ) -> Optional[Union[cp.File, cp.Emoji]]:

        if not icon_dict:
            return None

        if icon_dict["type"] == "emoji":
            return cp.Emoji.from_dict(icon_dict)
        return cp.File.from_dict(icon_dict)

    def _get_db_props(self, prop_dict: dict[str, Any]) -> Properties:

        props: Properties = Properties()
        for prop in prop_dict.values():
            try:
                prop_class = DB_PROPS_REVERSE_MAP[prop["type"]]
            except KeyError:
                prop_class = dbp.DBProp
            prop_instance = prop_class.from_dict(prop)

            props.add_prop(prop_instance)

        return props

    def _get_page_props(
        self, prop_dict: dict[str, Any], db: Optional[Database]
    ) -> Properties:

        props: Properties = Properties()
        for prop in prop_dict.values():

            try:
                prop_class = PAGE_PROPS_REVERSE_MAP[prop["type"]]
            except KeyError:
                prop_class = pgp.PProp
            prop_instance = prop_class.from_dict(prop)

            # Finding name if possible.
            # This is needed because the Notion API does not return
            # the name of preperty when retrieving a page.
            if db:
                prop_instance.name = db.properties._ids[prop_instance.id].name  # type: ignore

            props.add_prop(prop_instance)

        return props
