from notion.properties.common_properties import Option
from notion.properties.common_properties import StatusGroup
from notion.properties.db_properties import DBCheckbox
from notion.properties.db_properties import DBCreatedBy
from notion.properties.db_properties import DBCreatedTime
from notion.properties.db_properties import DBDate
from notion.properties.db_properties import DBEmail
from notion.properties.db_properties import DBFiles
from notion.properties.db_properties import DBFormula
from notion.properties.db_properties import DBLastEditedBy
from notion.properties.db_properties import DBLastEditedTime
from notion.properties.db_properties import DBMultiSelect
from notion.properties.db_properties import DBNumber
from notion.properties.db_properties import DBPhoneNumber
from notion.properties.db_properties import DBSelect
from notion.properties.db_properties import DBStatus
from notion.properties.db_properties import DBText
from notion.properties.db_properties import DBTitle
from notion.properties.db_properties import DBUrl
from notion.properties.prop_enums import NumberFormat
from notion.properties.prop_enums import PropTypes


def test_title_from_dict():

    title_dict = {"id": "title", "name": "Name", "type": "title", "title": {}}
    title = DBTitle.from_dict(title_dict)

    assert title.id == title_dict["id"]
    assert title.name == title_dict["name"]
    assert title.type == PropTypes.TITLE


def test_text_from_dict():

    text_dict = {"id": "hTKU", "name": "Text", "type": "rich_text", "rich_text": {}}
    text = DBText.from_dict(text_dict)

    assert text.id == text_dict["id"]
    assert text.name == text_dict["name"]
    assert text.type == PropTypes.RICH_TEXT


def test_date_from_dict():

    date_dict = {"id": "wx%3Ax", "name": "Date", "type": "date", "date": {}}
    date = DBDate.from_dict(date_dict)

    assert date.id == date_dict["id"]
    assert date.name == date_dict["name"]
    assert date.type == PropTypes.DATE


def test_files_from_dict():

    files_dict = {"id": "l%5Bht", "name": "Files & media", "type": "files", "files": {}}
    files = DBFiles.from_dict(files_dict)

    assert files.id == files_dict["id"]
    assert files.name == files_dict["name"]
    assert files.type == PropTypes.FILES


def test_checkbox_from_dict():

    checkbox_dict = {
        "id": "oBUr",
        "name": "Checkbox",
        "type": "checkbox",
        "checkbox": {},
    }
    checkbox = DBCheckbox.from_dict(checkbox_dict)

    assert checkbox.id == checkbox_dict["id"]
    assert checkbox.name == checkbox_dict["name"]
    assert checkbox.type == PropTypes.CHECKBOX


def test_url_from_dict():

    url_dict = {"id": "gafc", "name": "URL", "type": "url", "url": {}}
    url = DBUrl.from_dict(url_dict)

    assert url.id == url_dict["id"]
    assert url.name == url_dict["name"]
    assert url.type == PropTypes.URL


def test_email_from_dict():

    email_dict = {"id": "BxjB", "name": "Email", "type": "email", "email": {}}
    email = DBEmail.from_dict(email_dict)

    assert email.id == email_dict["id"]
    assert email.name == email_dict["name"]
    assert email.type == PropTypes.EMAIL


def test_phone_number_from_dict():

    phone_number_dict = {
        "id": "_%3Es%5E",
        "name": "Phone",
        "type": "phone_number",
        "phone_number": {},
    }
    phone_number = DBPhoneNumber.from_dict(phone_number_dict)

    assert phone_number.id == phone_number_dict["id"]
    assert phone_number.name == phone_number_dict["name"]
    assert phone_number.type == PropTypes.PHONE_NUMBER


def test_created_time_from_dict():

    created_time_dict = {
        "id": "HeeF",
        "name": "Created time",
        "type": "created_time",
        "created_time": {},
    }
    created_time = DBCreatedTime.from_dict(created_time_dict)

    assert created_time.id == created_time_dict["id"]
    assert created_time.name == created_time_dict["name"]
    assert created_time.type == PropTypes.CREATED_TIME


def test_created_by_from_dict():

    created_by_dict = {
        "id": "Dxuu",
        "name": "Created by",
        "type": "created_by",
        "created_by": {},
    }
    created_by = DBCreatedBy.from_dict(created_by_dict)

    assert created_by.id == created_by_dict["id"]
    assert created_by.name == created_by_dict["name"]
    assert created_by.type == PropTypes.CREATED_BY


def test_last_edited_time_from_dict():

    last_edited_time_dict = {
        "id": "Sq%3A%3D",
        "name": "Last edited time",
        "type": "last_edited_time",
        "last_edited_time": {},
    }
    last_edited_time = DBLastEditedTime.from_dict(last_edited_time_dict)

    assert last_edited_time.id == last_edited_time_dict["id"]
    assert last_edited_time.name == last_edited_time_dict["name"]
    assert last_edited_time.type == PropTypes.LAST_EDITED_TIME


def test_last_edited_by_from_dict():

    last_edited_by_dict = {
        "id": "xN~S",
        "name": "Last edited by",
        "type": "last_edited_by",
        "last_edited_by": {},
    }
    last_edited_by = DBLastEditedBy.from_dict(last_edited_by_dict)

    assert last_edited_by.id == last_edited_by_dict["id"]
    assert last_edited_by.name == last_edited_by_dict["name"]
    assert last_edited_by.type == PropTypes.LAST_EDITED_BY


def test_number_from_dict():

    number_dict = {
        "id": "l%5C%7BB",
        "name": "Number",
        "type": "number",
        "number": {"format": "number"},
    }
    number = DBNumber.from_dict(number_dict)

    assert number.id == number_dict["id"]
    assert number.name == number_dict["name"]
    assert number.type == PropTypes.NUMBER
    assert number.format == NumberFormat.NUMBER


def test_select_from_dict():

    select_dict = {
        "id": "TNsg",
        "name": "Select",
        "type": "select",
        "select": {
            "options": [
                {"id": "E>qs", "name": "Option Two", "color": "green"},
                {"id": "PLzY", "name": "Option One", "color": "blue"},
            ]
        },
    }
    select = DBSelect.from_dict(select_dict)

    assert select.id == select_dict["id"]
    assert select.name == select_dict["name"]
    assert select.type == PropTypes.SELECT
    assert len(select.options) == 2
    assert all((isinstance(opt, Option) for opt in select.options))


def test_multi_select_from_dict():

    multi_select_dict = {
        "id": "cco%7B",
        "name": "Multi-select",
        "type": "multi_select",
        "multi_select": {
            "options": [
                {
                    "id": "13b7de11-cbb0-4287-a9ce-ce92e0013df1",
                    "name": "Option One",
                    "color": "purple",
                },
                {
                    "id": "6b7a5abc-64bb-42af-ac34-df1407c8bdb9",
                    "name": "Option Two",
                    "color": "gray",
                },
            ]
        },
    }
    multi_select = DBMultiSelect.from_dict(multi_select_dict)

    assert multi_select.id == multi_select_dict["id"]
    assert multi_select.name == multi_select_dict["name"]
    assert multi_select.type == PropTypes.MULTI_SELECT
    assert len(multi_select.options) == 2
    assert all((isinstance(opt, Option) for opt in multi_select.options))


def test_status_from_dict():

    status_dict = {
        "id": "%7DELl",
        "name": "Status",
        "type": "status",
        "status": {
            "options": [
                {
                    "id": "835586e6-2e88-4914-8d98-6bf230ee1419",
                    "name": "Not started",
                    "color": "default",
                },
                {
                    "id": "e44864ef-9eb0-44bc-97fa-388bf98d9da9",
                    "name": "In progress",
                    "color": "blue",
                },
                {
                    "id": "9ebab972-c447-4b49-a7f3-ab67c1423446",
                    "name": "Done",
                    "color": "green",
                },
            ],
            "groups": [
                {
                    "id": "91370570-3bd0-4ce7-82ed-d857f0f95b03",
                    "name": "To-do",
                    "color": "gray",
                    "option_ids": ["835586e62e88-4914-8d98-6bf230ee1419"],
                },
                {
                    "id": "aae64de8-5dcf-4307-9365-8b14a1399d8a",
                    "name": "In progress",
                    "color": "blue",
                    "option_ids": ["e44864ef-9eb0-44bc-97fa-388bf98d9da9"],
                },
                {
                    "id": "610e7d45-6a39-4993-b21e-29cfa80cf6ae",
                    "name": "Complete",
                    "color": "green",
                    "option_ids": ["9ebab972-c447-4b49-a7f3-ab67c1423446"],
                },
            ],
        },
    }
    status = DBStatus.from_dict(status_dict)

    assert status.id == status_dict["id"]
    assert status.name == status_dict["name"]
    assert status.type == PropTypes.STATUS
    assert len(status.options) == 3
    assert all((isinstance(opt, Option) for opt in status.options))
    assert len(status.groups) == 3
    assert all((isinstance(grp, StatusGroup) for grp in status.groups))


def test_formula_from_dict():

    formula_dict = {
        "id": "%40OQ%3A",
        "name": "Formula",
        "type": "formula",
        "formula": {"expression": 'prop("Created time")'},
    }
    formula = DBFormula.from_dict(formula_dict)

    assert formula.id == formula_dict["id"]
    assert formula.name == formula_dict["name"]
    assert formula.type == PropTypes.FORMULA
    assert formula.expression == formula_dict["formula"]["expression"]
