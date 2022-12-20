from typing import Any

import nopy.props.db_props as dbp
from nopy.enums import NumberFormat
from nopy.enums import PropTypes


def test_checkbox():

    checkbox_args: dict[str, Any] = {
        "id": "K~Bk",
        "name": "Checkbox",
        "type": "checkbox",
        "checkbox": {},
    }
    checkbox = dbp.DBCheckbox.from_dict(checkbox_args)

    assert isinstance(checkbox, dbp.DBCheckbox)
    assert checkbox.id == checkbox_args["id"]
    assert checkbox.name == checkbox_args["name"]
    assert checkbox.type == PropTypes.CHECKBOX


def test_created_by():

    created_by_args: dict[str, Any] = {
        "id": "a%5E%40%3B",
        "name": "Created by",
        "type": "created_by",
        "created_by": {},
    }
    created_by = dbp.DBCreatedBy.from_dict(created_by_args)

    assert isinstance(created_by, dbp.DBCreatedBy)
    assert created_by.id == created_by_args["id"]
    assert created_by.name == created_by_args["name"]
    assert created_by.type == PropTypes.CREATED_BY


def test_created_time():

    created_time_args: dict[str, Any] = {
        "id": "jGDv",
        "name": "Created time",
        "type": "created_time",
        "created_time": {},
    }
    created_time = dbp.DBCreatedTime.from_dict(created_time_args)

    assert isinstance(created_time, dbp.DBCreatedTime)
    assert created_time.id == created_time_args["id"]
    assert created_time.name == created_time_args["name"]
    assert created_time.type == PropTypes.CREATED_TIME


def test_date():

    date_args: dict[str, Any] = {
        "id": "S%60%5Es",
        "name": "Date",
        "type": "date",
        "date": {},
    }
    date = dbp.DBDate.from_dict(date_args)

    assert isinstance(date, dbp.DBDate)
    assert date.id == date_args["id"]
    assert date.name == date_args["name"]
    assert date.type == PropTypes.DATE


def test_email():

    email_args: dict[str, Any] = {
        "id": "OUC%60",
        "name": "Email",
        "type": "email",
        "email": {},
    }
    email = dbp.DBEmail.from_dict(email_args)

    assert isinstance(email, dbp.DBEmail)
    assert email.id == email_args["id"]
    assert email.name == email_args["name"]
    assert email.type == PropTypes.EMAIL


def test_files():

    files_args: dict[str, Any] = {
        "id": "%3EK%7Bc",
        "name": "Files & media",
        "type": "files",
        "files": {},
    }
    files = dbp.DBFiles.from_dict(files_args)

    assert isinstance(files, dbp.DBFiles)
    assert files.id == files_args["id"]
    assert files.name == files_args["name"]
    assert files.type == PropTypes.FILES


def test_formula():

    formula_args: dict[str, Any] = {
        "id": "FjRK",
        "name": "Formula",
        "type": "formula",
        "formula": {"expression": 'prop("Name") + "hi"'},
    }
    formula = dbp.DBFormula.from_dict(formula_args)

    assert isinstance(formula, dbp.DBFormula)
    assert formula.id == formula_args["id"]
    assert formula.name == formula_args["name"]
    assert formula.type == PropTypes.FORMULA

    assert formula.expression == 'prop("Name") + "hi"'


def test_last_edited_by():

    last_edited_by_args: dict[str, Any] = {
        "id": "DLsP",
        "name": "Last edited by",
        "type": "last_edited_by",
        "last_edited_by": {},
    }
    last_edited_by = dbp.DBLastEditedBy.from_dict(last_edited_by_args)

    assert isinstance(last_edited_by, dbp.DBLastEditedBy)
    assert last_edited_by.id == last_edited_by_args["id"]
    assert last_edited_by.name == last_edited_by_args["name"]
    assert last_edited_by.type == PropTypes.LAST_EDITED_BY


def test_last_edited_time():

    last_edited_time_args: dict[str, Any] = {
        "id": "a%60gC",
        "name": "Last edited time",
        "type": "last_edited_time",
        "last_edited_time": {},
    }
    last_edited_time = dbp.DBLastEditedTime.from_dict(last_edited_time_args)

    assert isinstance(last_edited_time, dbp.DBLastEditedTime)
    assert last_edited_time.id == last_edited_time_args["id"]
    assert last_edited_time.name == last_edited_time_args["name"]
    assert last_edited_time.type == PropTypes.LAST_EDITED_TIME


def test_multi_select():

    multi_select_args: dict[str, Any] = {
        "id": "%3BFCu",
        "name": "Multi-select",
        "type": "multi_select",
        "multi_select": {"options": []},
    }
    multi_select = dbp.DBMultiSelect.from_dict(multi_select_args)

    assert isinstance(multi_select, dbp.DBMultiSelect)
    assert multi_select.id == multi_select_args["id"]
    assert multi_select.name == multi_select_args["name"]
    assert multi_select.type == PropTypes.MULTI_SELECT

    assert len(multi_select.options) == 0


def test_number():

    number_args: dict[str, Any] = {
        "id": "TqZn",
        "name": "Number",
        "type": "number",
        "number": {"format": "number"},
    }
    number = dbp.DBNumber.from_dict(number_args)

    assert isinstance(number, dbp.DBNumber)
    assert number.id == number_args["id"]
    assert number.name == number_args["name"]
    assert number.type == PropTypes.NUMBER

    assert number.format == NumberFormat.NUMBER


def test_people():

    people_args: dict[str, Any] = {
        "id": "R%5BgU",
        "name": "Person",
        "type": "people",
        "people": {},
    }
    people = dbp.DBPeople.from_dict(people_args)

    assert isinstance(people, dbp.DBPeople)
    assert people.id == people_args["id"]
    assert people.name == people_args["name"]
    assert people.type == PropTypes.PEOPLE


def test_phone_number():

    phone_number_args: dict[str, Any] = {
        "id": "SOCX",
        "name": "Phone",
        "type": "phone_number",
        "phone_number": {},
    }
    phone_number = dbp.DBPhoneNumber.from_dict(phone_number_args)

    assert isinstance(phone_number, dbp.DBPhoneNumber)
    assert phone_number.id == phone_number_args["id"]
    assert phone_number.name == phone_number_args["name"]
    assert phone_number.type == PropTypes.PHONE_NUMBER


def test_relation():

    relation_args: dict[str, Any] = {
        "id": "tnQq",
        "name": "Related Some Database",
        "type": "relation",
        "relation": {
            "database_id": "db-id",
            "type": "single_property",
            "single_property": {},
        },
    }
    relation = dbp.DBRelation.from_dict(relation_args)

    assert isinstance(relation, dbp.DBRelation)
    assert relation.id == relation_args["id"]
    assert relation.name == relation_args["name"]
    assert relation.type == PropTypes.RELATION

    assert relation.database_id == "db-id"
    assert relation.relation_type == "single_property"
    assert relation.synced_property_id is None
    assert relation.synced_property_name is None


def test_rollup():

    rollup_args: dict[str, Any] = {
        "id": "%7C%3Fd%3A",
        "name": "Rollup",
        "type": "rollup",
        "rollup": {
            "rollup_property_name": "Name",
            "relation_property_name": "Related Some Database",
            "rollup_property_id": "title",
            "relation_property_id": "tnQq",
            "function": "count",
        },
    }
    rollup = dbp.DBRollup.from_dict(rollup_args)

    assert isinstance(rollup, dbp.DBRollup)
    assert rollup.id == rollup_args["id"]
    assert rollup.name == rollup_args["name"]
    assert rollup.type == PropTypes.ROLLUP

    assert rollup.rollup_property_id == "title"
    assert rollup.rollup_property_name == "Name"
    assert rollup.relation_property_id == "tnQq"
    assert rollup.relation_property_name == "Related Some Database"
    assert rollup.function == "count"


def test_rich_text():

    rich_text_args: dict[str, Any] = {
        "id": "%3Cy%3A%5B",
        "name": "Text",
        "type": "rich_text",
        "rich_text": {},
    }
    rich_text = dbp.DBText.from_dict(rich_text_args)

    assert isinstance(rich_text, dbp.DBText)
    assert rich_text.id == rich_text_args["id"]
    assert rich_text.name == rich_text_args["name"]
    assert rich_text.type == PropTypes.RICH_TEXT


def test_select():

    select_args: dict[str, Any] = {
        "id": "ewCq",
        "name": "Select",
        "type": "select",
        "select": {
            "options": [{"id": "e`gS", "name": "Option One", "color": "yellow"}]
        },
    }
    select = dbp.DBSelect.from_dict(select_args)

    assert isinstance(select, dbp.DBSelect)
    assert select.id == select_args["id"]
    assert select.name == select_args["name"]
    assert select.type == PropTypes.SELECT

    assert len(select.options) == 1


def test_status():

    status_args: dict[str, Any] = {
        "id": "%3CxiG",
        "name": "Status",
        "type": "status",
        "status": {
            "options": [
                {"id": "option-one", "name": "Not started", "color": "default"},
                {"id": "option-two", "name": "In progress", "color": "blue"},
                {"id": "option-three", "name": "Done", "color": "green"},
            ],
            "groups": [
                {
                    "id": "group-one",
                    "name": "To-do",
                    "color": "gray",
                    "option_ids": ["option-one"],
                },
                {
                    "id": "group-two",
                    "name": "In progress",
                    "color": "blue",
                    "option_ids": ["option-two"],
                },
                {
                    "id": "group-three",
                    "name": "Complete",
                    "color": "green",
                    "option_ids": ["option-three"],
                },
            ],
        },
    }
    status = dbp.DBStatus.from_dict(status_args)

    assert isinstance(status, dbp.DBStatus)
    assert status.id == status_args["id"]
    assert status.name == status_args["name"]
    assert status.type == PropTypes.STATUS

    assert len(status.options) == 3
    assert len(status.groups) == 3


def test_url():

    url_args: dict[str, Any] = {
        "id": "%3BIa%40",
        "name": "URL",
        "type": "url",
        "url": {},
    }
    url = dbp.DBUrl.from_dict(url_args)

    assert isinstance(url, dbp.DBUrl)
    assert url.id == url_args["id"]
    assert url.name == url_args["name"]
    assert url.type == PropTypes.URL
