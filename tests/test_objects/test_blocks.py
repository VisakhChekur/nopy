from typing import Any

import pytest

import nopy.objects.blocks as blocks
from nopy.enums import BlockTypes
from nopy.enums import Colors
from nopy.enums import HeadingLevel
from nopy.enums import ListTypes
from nopy.enums import MediaTypes
from nopy.enums import ObjectTypes
from nopy.props.common import Emoji
from nopy.props.common import File


@pytest.fixture
def block_base_args():

    return {
        "object": "block",
        "id": "block-id",
        "parent": {"type": "page_id", "page_id": "page-id"},
        "created_time": "2023-01-07T10:43:00.000Z",
        "last_edited_time": "2023-01-07T11:26:00.000Z",
        "created_by": {"object": "user", "id": "user-id"},
        "last_edited_by": {"object": "user", "id": "user-id"},
        "archived": False,
    }


def test_paragraph(block_base_args: dict[str, Any]):

    paragraph_args = {
        "has_children": True,
        "type": "paragraph",
        "paragraph": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {"content": "test block", "link": None},
                    "annotations": {
                        "bold": False,
                        "italic": False,
                        "strikethrough": False,
                        "underline": False,
                        "code": False,
                        "color": "default",
                    },
                    "plain_text": "test block",
                    "href": None,
                }
            ],
            "color": "default",
        },
    }
    paragraph_args.update(block_base_args)
    para = blocks.Block.from_dict(paragraph_args)

    assert isinstance(para, blocks.Paragraph)
    assert para.id == "block-id"
    assert para.type == ObjectTypes.BLOCK

    assert para.block_type == BlockTypes.PARAGRAPH
    assert para.text == "test block"
    assert para.color == Colors.DEFAULT
    assert para.has_children is True


def test_heading(block_base_args: dict[str, Any]):

    heading_args = {
        "has_children": True,
        "type": "heading_1",
        "heading_1": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {"content": "Toggleable Level One Heading", "link": None},
                    "annotations": {
                        "bold": False,
                        "italic": False,
                        "strikethrough": False,
                        "underline": False,
                        "code": False,
                        "color": "default",
                    },
                    "plain_text": "Toggleable Level One Heading",
                    "href": None,
                }
            ],
            "is_toggleable": True,
            "color": "default",
        },
    }
    heading_args.update(block_base_args)
    heading = blocks.Block.from_dict(heading_args)

    assert isinstance(heading, blocks.Heading)
    assert heading.id == "block-id"
    assert heading.type == ObjectTypes.BLOCK

    assert heading.block_type == BlockTypes.HEADING
    assert heading.heading_level == HeadingLevel.HEADING_1
    assert heading.text == "Toggleable Level One Heading"
    assert heading.color == Colors.DEFAULT
    assert heading.has_children is True
    assert heading.is_toggleable is True


def test_callout(block_base_args: dict[str, Any]):

    callout_args = {
        "has_children": False,
        "type": "callout",
        "callout": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {"content": "Stuff", "link": None},
                    "annotations": {
                        "bold": False,
                        "italic": False,
                        "strikethrough": False,
                        "underline": False,
                        "code": False,
                        "color": "default",
                    },
                    "plain_text": "Stuff",
                    "href": None,
                }
            ],
            "icon": {"type": "emoji", "emoji": "\ud83d\udca1"},
            "color": "gray_background",
        },
    }
    callout_args.update(block_base_args)
    callout = blocks.Block.from_dict(callout_args)

    assert isinstance(callout, blocks.Callout)
    assert callout.id == "block-id"
    assert callout.type == ObjectTypes.BLOCK

    assert callout.block_type == BlockTypes.CALLOUT
    assert callout.text == "Stuff"
    assert callout.color == Colors.GRAY_BACKGROUND
    assert isinstance(callout.icon, Emoji)
    assert callout.icon.emoji == "\ud83d\udca1"
    assert callout.has_children is False


def test_quote(block_base_args: dict[str, Any]):

    quote_args = {
        "has_children": False,
        "type": "quote",
        "quote": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {"content": "Something deep and meaningful.", "link": None},
                    "annotations": {
                        "bold": False,
                        "italic": False,
                        "strikethrough": False,
                        "underline": False,
                        "code": False,
                        "color": "default",
                    },
                    "plain_text": "Something deep and meaningful.",
                    "href": None,
                }
            ],
            "color": "default",
        },
    }

    quote_args.update(block_base_args)
    quote = blocks.Block.from_dict(quote_args)

    assert isinstance(quote, blocks.Quote)
    assert quote.id == "block-id"
    assert quote.type == ObjectTypes.BLOCK

    assert quote.block_type == BlockTypes.QUOTE
    assert quote.text == "Something deep and meaningful."
    assert quote.color == Colors.DEFAULT
    assert quote.has_children is False


def test_list(block_base_args: dict[str, Any]):

    list_args = {
        "has_children": False,
        "type": "bulleted_list_item",
        "bulleted_list_item": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {"content": "item one", "link": None},
                    "annotations": {
                        "bold": False,
                        "italic": False,
                        "strikethrough": False,
                        "underline": False,
                        "code": False,
                        "color": "default",
                    },
                    "plain_text": "item one",
                    "href": None,
                }
            ],
            "color": "default",
        },
    }

    list_args.update(block_base_args)
    list_block = blocks.Block.from_dict(list_args)

    assert isinstance(list_block, blocks.List)
    assert list_block.id == "block-id"
    assert list_block.type == ObjectTypes.BLOCK

    assert list_block.block_type == BlockTypes.LIST
    assert list_block.text == "item one"
    assert list_block.color == Colors.DEFAULT
    assert list_block.list_type == ListTypes.BULLETED_LIST_ITEM
    assert list_block.has_children is False


def test_todo(block_base_args: dict[str, Any]):

    todo_args = {
        "has_children": False,
        "type": "to_do",
        "to_do": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {"content": "todo list item one", "link": None},
                    "annotations": {
                        "bold": False,
                        "italic": False,
                        "strikethrough": False,
                        "underline": False,
                        "code": False,
                        "color": "default",
                    },
                    "plain_text": "todo list item one",
                    "href": None,
                }
            ],
            "checked": False,
            "color": "default",
        },
    }

    todo_args.update(block_base_args)
    todo = blocks.Block.from_dict(todo_args)

    assert isinstance(todo, blocks.Todo)
    assert todo.id == "block-id"
    assert todo.type == ObjectTypes.BLOCK

    assert todo.block_type == BlockTypes.TO_DO
    assert todo.text == "todo list item one"
    assert todo.color == Colors.DEFAULT
    assert todo.has_children is False
    assert todo.checked is False


def test_toggle(block_base_args: dict[str, Any]):

    toggle_args = {
        "has_children": False,
        "type": "toggle",
        "toggle": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {"content": "toggle", "link": None},
                    "annotations": {
                        "bold": False,
                        "italic": False,
                        "strikethrough": False,
                        "underline": False,
                        "code": False,
                        "color": "default",
                    },
                    "plain_text": "toggle",
                    "href": None,
                }
            ],
            "color": "default",
        },
    }

    toggle_args.update(block_base_args)
    toggle = blocks.Block.from_dict(toggle_args)

    assert isinstance(toggle, blocks.Toggle)
    assert toggle.id == "block-id"
    assert toggle.type == ObjectTypes.BLOCK

    assert toggle.block_type == BlockTypes.TOGGLE
    assert toggle.text == "toggle"
    assert toggle.color == Colors.DEFAULT
    assert toggle.has_children is False


def test_code(block_base_args: dict[str, Any]):

    code_args = {
        "has_children": False,
        "type": "code",
        "code": {
            "caption": [
                {
                    "type": "text",
                    "text": {"content": "A sample Python program.", "link": None},
                    "annotations": {
                        "bold": False,
                        "italic": False,
                        "strikethrough": False,
                        "underline": False,
                        "code": False,
                        "color": "default",
                    },
                    "plain_text": "A sample Python program.",
                    "href": None,
                }
            ],
            "rich_text": [
                {
                    "type": "text",
                    "text": {"content": 'print("Hello world")', "link": None},
                    "annotations": {
                        "bold": False,
                        "italic": False,
                        "strikethrough": False,
                        "underline": False,
                        "code": False,
                        "color": "default",
                    },
                    "plain_text": 'print("Hello world")',
                    "href": None,
                }
            ],
            "language": "python",
        },
    }

    code_args.update(block_base_args)
    code = blocks.Block.from_dict(code_args)

    assert isinstance(code, blocks.Code)
    assert code.id == "block-id"
    assert code.type == ObjectTypes.BLOCK

    assert code.block_type == BlockTypes.CODE
    assert code.code == 'print("Hello world")'
    assert code.caption == "A sample Python program."
    assert code.language == "python"
    assert code.has_children is False


def test_child_page(block_base_args: dict[str, Any]):

    child_page_args = {
        "has_children": True,
        "type": "child_page",
        "child_page": {"title": "Blocks Examples"},
    }
    child_page_args.update(block_base_args)
    child_page = blocks.Block.from_dict(child_page_args)

    assert isinstance(child_page, blocks.ChildPage)
    assert child_page.id == "block-id"
    assert child_page.type == ObjectTypes.BLOCK

    assert child_page.title == "Blocks Examples"
    assert child_page.block_type == BlockTypes.CHILD_PAGE


def test_child_db(block_base_args: dict[str, Any]):

    child_db_args = {
        "has_children": True,
        "type": "child_database",
        "child_database": {"title": "Blocks Examples"},
    }
    child_db_args.update(block_base_args)
    child_db = blocks.Block.from_dict(child_db_args)

    assert isinstance(child_db, blocks.ChildDatabase)
    assert child_db.id == "block-id"
    assert child_db.type == ObjectTypes.BLOCK

    assert child_db.title == "Blocks Examples"
    assert child_db.block_type == BlockTypes.CHILD_DATABASE


def test_file(block_base_args: dict[str, Any]):

    file_args = {
        "has_children": False,
        "type": "file",
        "file": {
            "caption": [
                {
                    "type": "text",
                    "text": {"content": "Itachi Uchiha", "link": None},
                    "annotations": {
                        "bold": False,
                        "italic": False,
                        "strikethrough": False,
                        "underline": False,
                        "code": False,
                        "color": "default",
                    },
                    "plain_text": "Itachi Uchiha",
                    "href": None,
                }
            ],
            "type": "file",
            "file": {"url": "file-url", "expiry_time": "2023-01-07T15:28:56.320Z"},
        },
    }
    file_args.update(block_base_args)
    file_block = blocks.Block.from_dict(file_args)

    assert isinstance(file_block, blocks.Media)
    assert file_block.id == "block-id"
    assert file_block.type == ObjectTypes.BLOCK

    assert file_block.media_type == MediaTypes.FILE
    assert file_block.caption == "Itachi Uchiha"
    assert isinstance(file_block.media, File)


def test_image(block_base_args: dict[str, Any]):

    file_args = {
        "has_children": False,
        "type": "image",
        "image": {
            "caption": [
                {
                    "type": "text",
                    "text": {"content": "Pain", "link": None},
                    "annotations": {
                        "bold": False,
                        "italic": False,
                        "strikethrough": False,
                        "underline": False,
                        "code": False,
                        "color": "default",
                    },
                    "plain_text": "Pain",
                    "href": None,
                }
            ],
            "type": "file",
            "file": {"url": "file-url", "expiry_time": "2023-01-07T15:31:12.926Z"},
        },
    }
    file_args.update(block_base_args)
    file_block = blocks.Block.from_dict(file_args)

    assert isinstance(file_block, blocks.Media)
    assert file_block.id == "block-id"
    assert file_block.type == ObjectTypes.BLOCK

    assert file_block.media_type == MediaTypes.IMAGE
    assert file_block.caption == "Pain"
    assert isinstance(file_block.media, File)


def test_video(block_base_args: dict[str, Any]):

    file_args: dict[str, Any] = {
        "has_children": False,
        "type": "video",
        "video": {
            "caption": [],
            "type": "external",
            "external": {"url": "https://youtu.be/dQw4w9WgXcQ"},
        },
    }
    file_args.update(block_base_args)
    file_block = blocks.Block.from_dict(file_args)

    assert isinstance(file_block, blocks.Media)
    assert file_block.id == "block-id"
    assert file_block.type == ObjectTypes.BLOCK

    assert file_block.media_type == MediaTypes.VIDEO
    assert file_block.caption == ""
    assert isinstance(file_block.media, File)


def test_embed(block_base_args: dict[str, Any]):

    embed_args: dict[str, Any] = {
        "has_children": False,
        "type": "embed",
        "embed": {"url": "embed-url"},
    }
    embed_args.update(block_base_args)
    embed = blocks.Block.from_dict(embed_args)

    assert isinstance(embed, blocks.Embed)
    assert embed.id == "block-id"
    assert embed.type == ObjectTypes.BLOCK

    assert embed.block_type == BlockTypes.EMBED
    assert embed.url == "embed-url"


def test_bookmark(block_base_args: dict[str, Any]):

    bookmark_args: dict[str, Any] = {
        "has_children": False,
        "type": "bookmark",
        "bookmark": {"url": "bookmark-url"},
    }
    bookmark_args.update(block_base_args)
    bookmark = blocks.Block.from_dict(bookmark_args)

    assert isinstance(bookmark, blocks.Bookmark)
    assert bookmark.id == "block-id"
    assert bookmark.type == ObjectTypes.BLOCK

    assert bookmark.block_type == BlockTypes.BOOKMARK
    assert bookmark.url == "bookmark-url"
