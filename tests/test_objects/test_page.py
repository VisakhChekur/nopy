from datetime import datetime
from typing import Any

from nopy.enums import ObjectTypes
from nopy.objects.page import Page
from nopy.objects.user import User
from nopy.props.common import Emoji
from nopy.props.common import File
from nopy.props.common import PageParent


def test_normal_page(normal_page: dict[str, Any]):

    page = Page.from_dict(normal_page)

    assert page.type == ObjectTypes.PAGE

    assert page.id == "page-id"
    assert page.type == ObjectTypes.PAGE

    assert page.created_time == datetime.fromisoformat("2022-12-03T04:10:00.000Z")
    assert page.last_edited_time == datetime.fromisoformat("2022-12-20T03:01:00.000Z")
    assert isinstance(page.created_by, User)
    assert isinstance(page.last_edited_by, User)
    assert page.archived is False
    assert isinstance(page.parent, PageParent)

    assert page.title == "Trial Root Page"
    assert isinstance(page.icon, Emoji)
    assert isinstance(page.cover, File)
    assert page.url == "https://www.notion.so/page-id"


def test_page_properties(full_page: dict[str, Any]):

    page = Page.from_dict(full_page)
    page_props = full_page["properties"]

    # Subtracting 1 to deal with `title` property.
    assert len(page_props) - 1 == len(page.properties)

    for name, prop in page_props.items():

        prop_type = prop["type"]
        if prop_type == "title":
            continue

        assert prop["id"] in page.properties
        assert name in page.properties
        assert prop_type == page.properties[prop["id"]].type.value


def test_no_cover(normal_page: dict[str, Any]):

    normal_page["cover"] = None
    page = Page.from_dict(normal_page)

    assert page.cover is None


def test_no_icon(normal_page: dict[str, Any]):

    normal_page["icon"] = None
    page = Page.from_dict(normal_page)

    assert page.icon is None
