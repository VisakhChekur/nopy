import pytest
from notion.properties.db_props import *
from notion.properties.types_enums import Colors

pytestmark = pytest.mark.serialize

# ----- FIXTURES -----
@pytest.fixture
def options():

    return [Option("One", Colors.BLUE), Option("Two")]


# ----- TESTS -----
def test_title():

    title = DBTitle("Title")
    assert title.serialize() == {
        "title": {}
    }

def test_text():

    text = DBText("Text")
    assert text.serialize() == {
        "rich_text": {}
    }

def test_number():

    num = DBNumber("Number", NumberFormats.RUPEE)
    assert num.serialize() == {
        "number": {
            "format": "rupee"
        }
    }

def test_select(options: list[Option]):

    select = DBSelect("Select", options)
    assert select.serialize() == {
        "select": {
            "options": [
                {
                    "name": "One",
                    "color": "blue"
                },
                {
                    "name": "Two",
                    "color": "default"
                }
            ]
        }
    }

def test_multi_select(options: list[Option]):

    multi_select = DBMultiSelect("Multi Select", options)
    assert multi_select.serialize() == {
        "multi_select": {
            "options": [
                {
                    "name": "One",
                    "color": "blue"
                },
                {
                    "name": "Two",
                    "color": "default"
                }
            ]
        }
    }

def test_formula():

    formula = DBFormula("Formula", "formula string")
    assert formula.serialize() == {
        "formula": {
            "expression": "formula string"
        }
    }

def test_last_edited_by():

    last_edited_by = DBLastEditedBy("last_edited_by")
    assert last_edited_by.serialize() == {
        "last_edited_by": {}
    }

def test_last_edited_time():

    last_edited_time = DBLastEditedTime("last_edited_time")
    assert last_edited_time.serialize() == {
        "last_edited_time": {}
    }

def test_created_by():

    created_by = DBCreatedBy("created_by")
    assert created_by.serialize() == {
        "created_by": {}
    }

def test_created_time():

    created_time = DBCreatedTime("created_time")
    assert created_time.serialize() == {
        "created_time": {}
    }

def test_phone_number():

    phone_number = DBPhoneNumber("phone_number")
    assert phone_number.serialize() == {
        "phone_number": {}
    }

def test_email():

    email = DBEmail("email")
    assert email.serialize() == {
        "email": {}
    }

def test_url():

    url = DBUrl("url")
    assert url.serialize() == {
        "url": {}
    }

def test_checkbox():

    checkbox = DBCheckbox("checkbox")
    assert checkbox.serialize() == {
        "checkbox": {}
    }

def test_file():

    file = DBFile("file", File("some url"))
    assert file.serialize() == {
        "files": {}
    }

def test_people():

    people = DBPeople("people")
    assert people.serialize() == {
        "people": {}
    }

def test_date():

    date = DBDate("date")
    assert date.serialize() == {
        "date": {}
    }
