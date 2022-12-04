import pytest

from notion.properties import Annotations, RichText
from notion.properties.common import *

pytestmark = pytest.mark.serialize

# ----- FIXTURES -----

@pytest.fixture
def annotation():

    return Annotations(italic=True, underline=True)

@pytest.fixture
def rich_text(annotation: Annotations):

    return RichText("sample text", annotation)

# ----- TESTS ------

def test_annotations(annotation: Annotations):

    assert annotation.serialize() == {
        "bold": False,
        "italic": True,
        "underline": True,
        "code": False,
        "strikethrough": False
    }

def test_rich_text(rich_text: RichText):

    assert rich_text.serialize() == {
        "type": "text",
        "annotations": {
            "bold": False,
            "italic": True,
            "underline": True,
            "code": False,
            "strikethrough": False
        },
        "text": {
            "content": "sample text",
        }
    }

    rich_text.href = "some url"
    assert rich_text.serialize()["text"] == {
        "content": "sample text",
        "link": {
            "url": "some url"
        }
    }

def test_files():

    file = File("some url")
    assert file.serialize() == {
        "type": "external",
        "external": "some url"
    }

    file = File("some_url", FileTypes.FILE)
    with pytest.raises(UnsupportedError):
        file.serialize()