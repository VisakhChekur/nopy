from typing import Any

import pytest

from nopy.enums import NumberFormat
from nopy.enums import PropTypes
from nopy.exceptions import UnsupportedError
from nopy.properties import common_properties as cp
from nopy.properties import db_properties as dbp

# ----- Testing `from_dict` -----


def test_db_prop_fd():

    args: dict[str, Any] = {"name": "Property name", "id": "1"}
    db_prop = dbp.DBProp.from_dict(args)

    assert db_prop.name == "Property name"
    assert db_prop.id == "1"
    assert db_prop.type == PropTypes.UNSUPPORTED


def test_multi_select_fd():

    args: dict[str, Any] = {
        "id": "1",
        "name": "Multi-select",
        "type": "multi_select",
        "multi_select": {
            "options": [
                {"id": "]qMs", "name": "Option Two", "color": "brown"},
                {"id": "awLe", "name": "Option One", "color": "orange"},
            ]
        },
    }
    prop = dbp.DBMultiSelect.from_dict(args)

    assert prop.name == "Multi-select"
    assert prop.id == "1"
    assert len(prop.options) == 2
    assert all((isinstance(opt, cp.Option) for opt in prop.options))
    assert prop.type == PropTypes.MULTI_SELECT


def test_url_fd():

    args: dict[str, Any] = {"id": "1", "name": "URL", "type": "url", "url": {}}
    prop = dbp.DBUrl.from_dict(args)

    assert prop.name == "URL"
    assert prop.id == "1"
    assert prop.type == PropTypes.URL


def test_email_fd():

    args: dict[str, Any] = {"id": "1", "name": "Email", "type": "email", "email": {}}
    prop = dbp.DBEmail.from_dict(args)

    assert prop.name == "Email"
    assert prop.id == "1"
    assert prop.type == PropTypes.EMAIL


def test_checkbox_fd():

    args: dict[str, Any] = {
        "id": "1",
        "name": "Checkbox",
        "type": "checkbox",
        "checkbox": {},
    }
    prop = dbp.DBCheckbox.from_dict(args)

    assert prop.name == "Checkbox"
    assert prop.id == "1"
    assert prop.type == PropTypes.CHECKBOX


def test_text_fd():

    args: dict[str, Any] = {
        "id": "1",
        "name": "Text",
        "type": "rich_text",
        "rich_text": {},
    }
    prop = dbp.DBText.from_dict(args)

    assert prop.name == "Text"
    assert prop.id == "1"
    assert prop.type == PropTypes.RICH_TEXT


def test_last_edited_time_fd():

    args: dict[str, Any] = {
        "id": "1",
        "name": "Last edited time",
        "type": "last_edited_time",
        "last_edited_time": {},
    }
    prop = dbp.DBLastEditedTime.from_dict(args)

    assert prop.name == "Last edited time"
    assert prop.id == "1"
    assert prop.type == PropTypes.LAST_EDITED_TIME


def test_select_fp():

    args: dict[str, Any] = {
        "id": "1",
        "name": "Select",
        "type": "select",
        "select": {
            "options": [
                {"id": "]qMs", "name": "Option Two", "color": "brown"},
                {"id": "awLe", "name": "Option One", "color": "orange"},
            ]
        },
    }
    prop = dbp.DBSelect.from_dict(args)

    assert prop.name == "Select"
    assert prop.id == "1"
    assert prop.type == PropTypes.SELECT
    assert len(prop.options) == 2
    assert all(isinstance(opt, cp.Option) for opt in prop.options)


def test_formula_fd():

    args: dict[str, Any] = {
        "id": "1",
        "name": "Formula",
        "type": "formula",
        "formula": {"expression": "add(1, 2)"},
    }
    prop = dbp.DBFormula.from_dict(args)

    assert prop.name == "Formula"
    assert prop.id == "1"
    assert prop.type == PropTypes.FORMULA
    assert prop.expression == "add(1, 2)"


def test_formula_without_expression_df():

    args: dict[str, Any] = {
        "id": "1",
        "name": "Formula",
        "type": "formula",
        "formula": {"expression": ""},
    }
    prop = dbp.DBFormula.from_dict(args)
    assert prop.name == "Formula"
    assert prop.id == "1"
    assert prop.type == PropTypes.FORMULA
    assert prop.expression == ""


def test_date_fd():

    args: dict[str, Any] = {
        "id": "1",
        "name": "Date",
        "type": "date",
        "date": {},
    }
    prop = dbp.DBDate.from_dict(args)

    assert prop.name == "Date"
    assert prop.id == "1"
    assert prop.type == PropTypes.DATE


def test_files_fd():

    args: dict[str, Any] = {"id": "1", "name": "Files", "type": "files", "files": {}}
    prop = dbp.DBFiles.from_dict(args)

    assert prop.name == "Files"
    assert prop.id == "1"
    assert prop.type == PropTypes.FILES


def test_status_fd():

    args: dict[str, Any] = {
        "id": "1",
        "name": "Status",
        "type": "status",
        "status": {
            "options": [
                {
                    "id": "d8bdc387-814e-4329-957e-002040b165b0",
                    "name": "Not started",
                    "color": "default",
                },
                {
                    "id": "95a73d8d-6d8b-4ae0-ae94-618ddba17d9d",
                    "name": "In progress",
                    "color": "blue",
                },
                {
                    "id": "a8f17f85-b64d-4648-bec6-9de225ae970a",
                    "name": "Done",
                    "color": "green",
                },
            ],
            "groups": [
                {
                    "id": "12453c6d-9507-4d82-999e-5effeb2fbcff",
                    "name": "To-do",
                    "color": "gray",
                    "option_ids": ["d8bdc387-814e-4329-957e-002040b165b0"],
                },
                {
                    "id": "13cf3083-66a9-4a35-851f-a92a70911b93",
                    "name": "In progress",
                    "color": "blue",
                    "option_ids": ["95a73d8d-6d8b-4ae0-ae94-618ddba17d9d"],
                },
                {
                    "id": "c12e4526-c54a-4d6f-b6ca-add0cc6bdab2",
                    "name": "Complete",
                    "color": "green",
                    "option_ids": ["a8f17f85-b64d-4648-bec6-9de225ae970a"],
                },
            ],
        },
    }
    prop = dbp.DBStatus.from_dict(args)

    assert prop.name == "Status"
    assert prop.id == "1"
    assert prop.type == PropTypes.STATUS
    assert len(prop.options) == 3
    assert all((isinstance(opt, cp.Option) for opt in prop.options))
    assert len(prop.groups) == 3
    assert all((isinstance(grp, cp.StatusGroup) for grp in prop.groups))


def test_created_time_fd():

    args: dict[str, Any] = {
        "id": "1",
        "name": "Created time",
        "type": "created_time",
        "created_time": {},
    }
    prop = dbp.DBCreatedTime.from_dict(args)

    assert prop.name == "Created time"
    assert prop.id == "1"
    assert prop.type == PropTypes.CREATED_TIME


def test_phone_number_fd():

    args: dict[str, Any] = {
        "id": "1",
        "name": "Phone",
        "type": "phone_number",
        "phone_number": {},
    }
    prop = dbp.DBPhoneNumber.from_dict(args)

    assert prop.name == "Phone"
    assert prop.id == "1"
    assert prop.type == PropTypes.PHONE_NUMBER


def test_number_fd():

    args: dict[str, Any] = {
        "id": "1",
        "name": "Number",
        "type": "number",
        "number": {"format": "number"},
    }
    prop = dbp.DBNumber.from_dict(args)

    assert prop.name == "Number"
    assert prop.id == "1"
    assert prop.type == PropTypes.NUMBER
    assert prop.format == NumberFormat.NUMBER


def test_title_fd():

    args: dict[str, Any] = {
        "id": "title",
        "name": "Created DB",
        "type": "title",
        "title": {},
    }
    prop = dbp.DBTitle.from_dict(args)

    assert prop.name == "Created DB"
    assert prop.id == "title"
    assert prop.type == PropTypes.TITLE


# ------ Test `serialize` -----


def test_db_prop_serialize():

    with pytest.raises(UnsupportedError):
        dbp.DBProp("name").serialize()


# This one test is enough for all the properties without any extra properties
def test_serialize():

    prop = dbp.DBText("text")
    serialized = prop.serialize()

    assert serialized["name"] == prop.name
    assert "rich_text" in serialized
    assert serialized["rich_text"] == {}


def test_select_serialize(options: list[cp.Option]):

    prop = dbp.DBSelect("select", options=options)
    serialized = prop.serialize()

    assert serialized["name"] == prop.name
    assert "select" in serialized
    assert "options" in serialized["select"]
    assert isinstance(serialized["select"]["options"], list)
    assert len(serialized["select"]["options"]) == len(prop.options)


def test_multi_select_serialize(options: list[cp.Option]):

    prop = dbp.DBMultiSelect("multi select", options=options)
    serialized = prop.serialize()

    assert serialized["name"] == prop.name
    assert "multi_select" in serialized
    assert "options" in serialized["multi_select"]
    assert isinstance(serialized["multi_select"]["options"], list)
    assert len(serialized["multi_select"]["options"]) == len(prop.options)


def test_number_serialize():

    prop = dbp.DBNumber("number", format=NumberFormat.RUPEE)
    serialized = prop.serialize()

    assert serialized["name"] == prop.name
    assert "number" in serialized
    assert "format" in serialized["number"]
    assert serialized["number"]["format"] == prop.format.value
