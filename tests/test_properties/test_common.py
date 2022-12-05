from datetime import datetime

from notion.properties.common_properties import Annotations
from notion.properties.common_properties import BlockParent
from notion.properties.common_properties import DatabaseParent
from notion.properties.common_properties import Emoji
from notion.properties.common_properties import File
from notion.properties.common_properties import Option
from notion.properties.common_properties import PageParent
from notion.properties.common_properties import RichText
from notion.properties.common_properties import StatusGroup
from notion.properties.common_properties import Text
from notion.properties.common_properties import WorkspaceParent
from notion.properties.prop_enums import Colors
from notion.properties.prop_enums import EmojiTypes
from notion.properties.prop_enums import FileTypes
from notion.properties.prop_enums import ParentTypes
from notion.properties.prop_enums import RichTextTypes


# ----- `from_dict` Tests -----
def test_option_from_dict():

    option_dict = {"id": "ou@_", "name": "jQuery", "color": "purple"}
    option = Option.from_dict(option_dict)

    assert option.color == Colors.PURPLE
    assert option.name == option_dict["name"]
    assert option.id == option_dict["id"]


def test_status_from_dict():

    status_dict = {
        "id": "539f2705-6529-42d8-a215-61a7183a92c0",
        "name": "In progress",
        "color": "blue",
    }
    status = StatusGroup.from_dict(status_dict)

    assert status.id == status_dict["id"]
    assert status.name == status_dict["name"]
    assert status.color == Colors.BLUE


def test_annotations_from_dict():

    annot_dict = {
        "bold": True,
        "italic": False,
        "strikethrough": False,
        "underline": False,
        "code": False,
        "color": "default",
    }
    annot = Annotations.from_dict(annot_dict)

    assert annot.bold == True  # noqa
    assert annot.italic == False  # noqa
    assert annot.strikethrough == False  # noqa
    assert annot.underline == False  # noqa
    assert annot.code == False  # noqa
    assert annot.color == Colors.DEFAULT


def test_link_from_dict():
    pass


def test_rich_text_from_dict():

    rich_text_dict = {
        "type": "text",
        "text": {"content": "Test Database  ", "link": None},
        "annotations": {
            "bold": False,
            "italic": False,
            "strikethrough": False,
            "underline": False,
            "code": False,
            "color": "default",
        },
        "plain_text": "Test Database  ",  # don't remove whitespace
        "href": "sample href",
    }
    rich_text = RichText.from_dict(rich_text_dict)

    assert rich_text.plain_text == "Test Database"
    assert rich_text.href == "sample href"
    assert rich_text.type == RichTextTypes.UNSUPPORTED
    assert isinstance(rich_text.annotations, Annotations) == True  # noqa


def test_text_from_dict():

    rich_text_dict = {
        "type": "text",
        "text": {"content": "Test Database", "link": None},
        "annotations": {
            "bold": False,
            "italic": False,
            "strikethrough": False,
            "underline": False,
            "code": False,
            "color": "default",
        },
        "plain_text": "Test Database  ", # don't remove whitespace
        "href": "sample href",
    }
    rich_text = Text.from_dict(rich_text_dict)

    assert rich_text.plain_text == "Test Database"
    assert rich_text.href == "sample href"
    assert rich_text.type == RichTextTypes.TEXT
    assert isinstance(rich_text.annotations, Annotations) == True  # noqa


def test_external_file_from_dict():

    external_file_dict = {
        "type": "external",
        "external": {
            "url": "https://www.notion.so/images/page-cover/met_william_morris_1875.jpg"
        },
    }
    external = File.from_dict(external_file_dict)

    assert external.url == external_file_dict["external"]["url"]
    assert external.expiry_time is None
    assert external.type == FileTypes.EXTERNAL


def test_file_from_dict():

    file_dict = {
        "type": "file",
        "file": {
            "url": "https://www.notion.so/images/page-cover/met_william_morris_1875.jpg",
            "expiry_time": "2020-03-17T19:10:04.968Z",
        },
    }
    file_obj = File.from_dict(file_dict)

    assert file_obj.url == file_dict["file"]["url"]
    assert file_obj.type == FileTypes.FILE
    assert isinstance(file_obj.expiry_time, datetime)


def test_emoji_from_dict():

    emoji_dict = {"type": "emoji", "emoji": "\ud83c\udf0e"}
    emoji = Emoji.from_dict(emoji_dict)

    assert emoji.emoji == emoji_dict["emoji"]
    assert emoji.type == EmojiTypes.EMOJI


def test_db_parent_from_dict():

    db_parent_dict = {
        "type": "database_id",
        "database_id": "d9824bdc-8445-4327-be8b-5b47500af6ce",
    }
    db_parent = DatabaseParent.from_dict(db_parent_dict)

    assert db_parent.id == db_parent_dict["database_id"]
    assert db_parent.type == ParentTypes.DATABASE


def test_page_parent_from_dict():

    page_parent_dict = {
        "type": "page_id",
        "page_id": "59833787-2cf9-4fdf-8782-e53db20768a5",
    }
    page_parent = PageParent.from_dict(page_parent_dict)

    assert page_parent.id == page_parent_dict["page_id"]
    assert page_parent.type == ParentTypes.PAGE


def test_workspace_parent_from_dict():

    workspace_dict = {"type": "workspace", "workspace": True}
    workspace_parent = WorkspaceParent.from_dict(workspace_dict)

    assert workspace_parent.id == True  # noqa
    assert workspace_parent.type == ParentTypes.WORKSPACE


def test_block_parent_from_dict():

    block_parent_dict = {
        "type": "block_id",
        "block_id": "7d50a184-5bbe-4d90-8f29-6bec57ed817b",
    }
    block_parent = BlockParent.from_dict(block_parent_dict)

    assert block_parent.id == block_parent_dict["block_id"]
    assert block_parent.type == ParentTypes.BLOCK
