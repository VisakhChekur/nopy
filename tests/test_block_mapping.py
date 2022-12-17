import json
from datetime import datetime
from pathlib import Path
from typing import Any

import nopy.objects.blocks as blocks
import nopy.properties.common_properties as cp
from nopy.block_mapper import map_to_block
from nopy.enums import Colors
from nopy.enums import HeadingLevels
from nopy.objects.block_types import BlockTypes

data_fp = Path(__file__).parent / "test-data" / "blocks"


def common_checks(block: blocks.Block):

    assert block.id == "block-id"
    assert isinstance(block.created_time, datetime)
    assert isinstance(block.last_edited_time, datetime)
    assert not block.archived


def get_block(block_name: str) -> blocks.Block:

    fp = data_fp / (block_name + ".json")
    with open(fp, "r") as f:
        block_dict: dict[str, Any] = json.load(f)

    return map_to_block(block_dict)


def test_heading():

    heading = get_block("heading")
    assert isinstance(heading, blocks.Heading)

    # Common checks on all of the blocks
    common_checks(heading)
    assert isinstance(heading.parent, cp.PageParent)
    assert heading.parent.id == "page-id"

    assert heading.is_toggleable
    assert heading.has_children
    assert heading.heading == "Toggled Heading"
    assert heading.color == Colors.DEFAULT
    assert heading.heading_level == HeadingLevels.HEADING_2
    assert all((isinstance(rt, cp.Text) for rt in heading.rich_heading))
    assert heading.type == BlockTypes.HEADING


def test_paragraph():

    para = get_block("paragraph")
    assert isinstance(para, blocks.Paragraph)

    common_checks(para)
    assert isinstance(para.parent, cp.PageParent)
    assert para.parent.id == "page-id"

    assert not para.has_children
    assert para.paragraph == """A paragraph about some awesome stuff"""
    assert para.color == Colors.DEFAULT
    assert para.type == BlockTypes.PARAGRAPH


def test_callout():

    callout = get_block("callout")
    assert isinstance(callout, blocks.Callout)

    common_checks(callout)
    assert isinstance(callout.parent, cp.PageParent)
    assert callout.parent.id == "page-id"

    assert not callout.has_children
    assert callout.callout == "I'm calling you out."
    assert isinstance(callout.icon, cp.Emoji)
    assert callout.color == Colors.GRAY_BACKGROUND
    assert callout.type == BlockTypes.CALLOUT


def test_quote():

    quote = get_block("quote")
    assert isinstance(quote, blocks.Quote)

    common_checks(quote)
    assert isinstance(quote.parent, cp.PageParent)
    assert quote.parent.id == "page-id"

    assert not quote.has_children
    assert quote.quote == "Some profound quote."
    assert quote.color == Colors.DEFAULT
    assert quote.type == BlockTypes.QUOTE


def test_bullet_list():

    bullet = get_block("bulleted_list")
    assert isinstance(bullet, blocks.BulletList)

    common_checks(bullet)
    assert isinstance(bullet.parent, cp.PageParent)
    assert bullet.parent.id == "page-id"

    assert bullet.item == "one"
    assert bullet.color == Colors.DEFAULT
    assert bullet.type == BlockTypes.BULLETED_LIST_ITEM


def test_number_list():

    number = get_block("numbered_list")
    assert isinstance(number, blocks.NumberedList)

    common_checks(number)
    assert isinstance(number.parent, cp.PageParent)
    assert number.parent.id == "page-id"

    assert number.item == "one numbered"
    assert number.color == Colors.DEFAULT
    assert number.type == BlockTypes.NUMBERED_LIST_ITEM


def test_todo():

    todo = get_block("todo")
    assert isinstance(todo, blocks.Todo)

    common_checks(todo)
    assert isinstance(todo.parent, cp.PageParent)
    assert todo.parent.id == "page-id"

    assert todo.item == "do this"
    assert not todo.checked
    assert todo.color == Colors.DEFAULT
    assert todo.type == BlockTypes.TO_DO
