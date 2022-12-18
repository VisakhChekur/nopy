from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from nopy.enums import Colors
from nopy.enums import FileTypes
from nopy.enums import MentionTypes
from nopy.enums import RichTextTypes
from nopy.props.common import Annotations
from nopy.props.common import Date
from nopy.props.common import Emoji
from nopy.props.common import Equation
from nopy.props.common import File
from nopy.props.common import Link
from nopy.props.common import Mention
from nopy.props.common import Option
from nopy.props.common import RichText
from nopy.props.common import Text

# ----- Testing `from_dict` -----


def test_annotations_fd():

    args: dict[str, Any] = {
        "bold": False,
        "italic": False,
        "strikethrough": False,
        "underline": False,
        "code": False,
        "color": "default",
    }
    annot = Annotations.from_dict(args)

    assert annot.bold is False
    assert annot.italic is False
    assert annot.strikethrough is False
    assert annot.underline is False
    assert annot.code is False
    assert annot.color == Colors.DEFAULT


def test_date_fd():

    args: dict[str, Any] = {
        "start": "2022-12-18",
        "end": None,
        "time_zone": "America/Los_Angeles",
    }
    date = Date.from_dict(args)

    assert isinstance(date, Date)
    assert date.start == datetime.fromisoformat("2022-12-18")
    assert date.end is None
    assert date.time_zone == ZoneInfo("America/Los_Angeles")


def test_link_fd():

    args: dict[str, Any] = {
        "url": "some url",
    }
    link = Link.from_dict(args)

    assert isinstance(link, Link)
    assert link.url == "some url"


def test_text_fd():

    args: dict[str, Any] = {
        "type": "text",
        "text": {"content": "Database Example", "link": {"url": "some url"}},
        "annotations": {
            "bold": False,
            "italic": False,
            "strikethrough": False,
            "underline": False,
            "code": False,
            "color": "default",
        },
        "plain_text": "Database Example",
        "href": None,
    }
    text = RichText.from_dict(args)

    assert isinstance(text, Text)
    assert text.type == RichTextTypes.TEXT

    assert text.plain_text == "Database Example"
    assert text.href is None
    assert isinstance(text.annotations, Annotations)
    assert isinstance(text.link, Link)


def test_db_mention_fd():

    args: dict[str, Any] = {
        "type": "mention",
        "mention": {"type": "database", "database": {"id": "db-id"}},
        "annotations": {
            "bold": False,
            "italic": False,
            "strikethrough": False,
            "underline": False,
            "code": False,
            "color": "default",
        },
        "plain_text": "Database mention",
        "href": "some url",
    }
    mention = RichText.from_dict(args)

    assert isinstance(mention, Mention)
    assert mention.type == RichTextTypes.MENTION
    assert mention.plain_text == "Database mention"
    assert mention.href == "some url"
    assert isinstance(mention.annotations, Annotations)
    assert mention.mention_type == MentionTypes.DATABASE
    assert mention.id == "db-id"


def test_date_mention_fd():

    args: dict[str, Any] = {
        "type": "mention",
        "mention": {
            "type": "date",
            "date": {"start": "2022-12-18", "end": None, "time_zone": None},
        },
        "annotations": {
            "bold": False,
            "italic": False,
            "strikethrough": False,
            "underline": False,
            "code": False,
            "color": "default",
        },
        "plain_text": "2022-12-18",
        "href": None,
    }
    mention = RichText.from_dict(args)

    assert isinstance(mention, Mention)
    assert mention.type == RichTextTypes.MENTION
    assert mention.plain_text == "2022-12-18"
    assert mention.href is None
    assert isinstance(mention.annotations, Annotations)
    assert mention.mention_type == MentionTypes.DATE
    assert isinstance(mention.date, Date)


def test_equation_fd():

    args: dict[str, Any] = {
        "type": "equation",
        "equation": {"expression": "x = 5"},
        "annotations": {
            "bold": False,
            "italic": False,
            "strikethrough": False,
            "underline": False,
            "code": False,
            "color": "default",
        },
        "plain_text": "x = 5",
        "href": None,
    }
    equation = RichText.from_dict(args)

    assert isinstance(equation, Equation)
    assert equation.type == RichTextTypes.EQUATION

    assert equation.plain_text == "x = 5"
    assert equation.href is None
    assert isinstance(equation.annotations, Annotations)
    assert equation.expression == "x = 5"


def test_file_fd():

    args: dict[str, Any] = {
        "type": "file",
        "file": {"url": "some url", "expiry_time": "2022-12-18T16:11:41.373Z"},
    }
    file = File.from_dict(args)

    assert file.url == "some url"
    assert file.type == FileTypes.FILE
    assert file.expiry_time == datetime.fromisoformat("2022-12-18T16:11:41.373Z")


def test_option_fd():

    args: dict[str, Any] = {
        "id": "option-id",
        "name": "Not started",
        "color": "default",
    }
    option = Option.from_dict(args)

    assert option.id == "option-id"
    assert option.name == "Not started"
    assert option.color == Colors.DEFAULT


def test_emoji_fd():

    args: dict[str, Any] = {"type": "emoji", "emoji": "\ud83c\udf8a"}
    emoji = Emoji.from_dict(args)

    assert emoji.emoji == "\ud83c\udf8a"
