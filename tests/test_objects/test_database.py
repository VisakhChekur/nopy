from datetime import datetime
from typing import Any

from nopy.enums import ObjectTypes
from nopy.objects.database import Database
from nopy.objects.user import User
from nopy.props.common import Emoji
from nopy.props.common import PageParent


def test_full_db(full_db: dict[str, Any]):

    db = Database.from_dict(full_db)

    assert db.id == "db-id"
    assert db.type == ObjectTypes.DATABASE

    assert db.created_time == datetime.fromisoformat("2022-12-18T07:28:00.000Z")
    assert db.last_edited_time == datetime.fromisoformat("2022-12-18T15:11:00.000Z")
    assert isinstance(db.created_by, User)
    assert isinstance(db.last_edited_by, User)
    assert db.archived is False
    assert isinstance(db.parent, PageParent)

    assert db.title == "Database Example"
    assert db.description == ""
    assert isinstance(db.icon, Emoji)
    assert db.is_inline is True
    assert db.url == "https://www.notion.so/db-id"


def test_db_properties(full_db: dict[str, Any]):

    db = Database.from_dict(full_db)
    db_props = full_db["properties"]

    # Subtracting 1 to deal with `title` property.
    assert len(db_props) - 1 == len(db.properties)

    for prop in db_props.values():

        prop_type = prop["type"]
        if prop_type == "title":
            continue

        assert prop["id"] in db.properties
        assert prop_type == db.properties[prop["id"]].type.value


def test_no_cover(full_db: dict[str, Any]):

    full_db["cover"] = None
    db = Database.from_dict(full_db)

    assert db.cover is None


def test_no_icon(full_db: dict[str, Any]):

    full_db["icon"] = None
    db = Database.from_dict(full_db)

    assert db.icon is None


def test_no_title(full_db: dict[str, Any]):

    full_db["title"] = []
    db = Database.from_dict(full_db)

    assert db.title == ""
    assert len(db.rich_title) == 0
