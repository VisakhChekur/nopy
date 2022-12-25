from datetime import datetime
from typing import Any

import nopy.props.page_props as pgp
from nopy.enums import Colors
from nopy.enums import PropTypes
from nopy.enums import RollupFunctions
from nopy.objects.user import Person
from nopy.props.common import Date
from nopy.props.common import File
from nopy.props.common import Option


def test_checkbox_fd():

    checkbox_args: dict[str, Any] = {
        "id": "_PxG",
        "type": "checkbox",
        "checkbox": False,
    }
    checkbox: pgp.PCheckbox = pgp.PCheckbox.from_dict(checkbox_args)

    assert checkbox.type == PropTypes.CHECKBOX
    assert checkbox.id == checkbox_args["id"]

    assert checkbox.checked is False


def test_created_by_fd():

    created_by_args: dict[str, Any] = {
        "id": "iAaH",
        "type": "created_by",
        "created_by": {
            "object": "user",
            "id": "user-id",
            "name": "guacs",
            "avatar_url": "image url",
            "type": "person",
            "person": {"email": "user@awesome.com"},
        },
    }
    created_by: pgp.PCreatedby = pgp.PCreatedby.from_dict(created_by_args)

    assert created_by.type == PropTypes.CREATED_BY
    assert created_by.id == created_by_args["id"]

    assert isinstance(created_by.created_by, Person)
    assert created_by.created_by.name == "guacs"
    assert created_by.created_by.id == "user-id"


def test_created_time_fd():

    created_time_args: dict[str, Any] = {
        "id": "I%40aJ",
        "type": "created_time",
        "created_time": "2022-12-23T08:50:00.000Z",
    }
    created_time: pgp.PCreatedTime = pgp.PCreatedTime.from_dict(created_time_args)

    assert created_time.type == PropTypes.CREATED_TIME
    assert created_time.id == created_time_args["id"]

    assert created_time.created_time == datetime.fromisoformat(
        created_time_args["created_time"]
    )


def test_date_fd():

    date_args: dict[str, Any] = {
        "id": "%5B%3BFA",
        "type": "date",
        "date": {
            "start": "2022-12-29T00:00:00.000+05:30",
            "end": None,
            "time_zone": None,
        },
    }
    date: pgp.PDate = pgp.PDate.from_dict(date_args)

    assert date.type == PropTypes.DATE
    assert date.id == date_args["id"]

    assert isinstance(date.date, Date)


def test_date_empty_fd():

    date_args: dict[str, Any] = {"id": "%5B%3BFA", "type": "date", "date": None}
    date: pgp.PDate = pgp.PDate.from_dict(date_args)

    assert date.date is None


def test_email_fd():

    email_args: dict[str, Any] = {
        "id": "YOM%7B",
        "type": "email",
        "email": "user@awesome.com",
    }
    email: pgp.PEmail = pgp.PEmail.from_dict(email_args)

    assert email.type == PropTypes.EMAIL
    assert email.id == email_args["id"]

    assert email.email == "user@awesome.com"


def test_email_empty__fd():

    email_args: dict[str, Any] = {
        "id": "YOM%7B",
        "type": "email",
        "email": None,
    }
    email: pgp.PEmail = pgp.PEmail.from_dict(email_args)

    assert email.type == PropTypes.EMAIL
    assert email.id == email_args["id"]

    assert email.email is None


def test_files_fd():

    files_args: dict[str, Any] = {
        "id": "%3CIjy",
        "type": "files",
        "files": [
            {
                "name": "itachi-anbu.jpg",
                "type": "file",
                "file": {"url": "some url", "expiry_time": "2022-12-25T08:00:06.090Z"},
            }
        ],
    }
    files: pgp.PFiles = pgp.PFiles.from_dict(files_args)

    assert files.type == PropTypes.FILES
    assert files.id == files_args["id"]

    assert len(files.files) == 1
    assert all((isinstance(file, File) for file in files.files))


def test_formula_fd():

    formula_args: dict[str, Any] = {
        "id": "%40EE%7B",
        "type": "formula",
        "formula": {"type": "number", "number": 3},
    }
    formula: pgp.PFormula = pgp.PFormula.from_dict(formula_args)

    assert formula.type == PropTypes.FORMULA
    assert formula.id == formula_args["id"]

    assert formula.value_type == "number"
    assert formula.value == 3


def test_formula_empty__fd():

    formula_args: dict[str, Any] = {
        "id": "%40EE%7B",
        "type": "formula",
        "formula": {"type": "string", "string": None},
    }
    formula: pgp.PFormula = pgp.PFormula.from_dict(formula_args)

    assert formula.value_type == "string"
    assert formula.value is None


def test_last_edited_by_fd():

    last_edited_by_args: dict[str, Any] = {
        "id": "iAaH",
        "type": "last_edited_by",
        "last_edited_by": {
            "object": "user",
            "id": "user-id",
            "name": "guacs",
            "avatar_url": "image url",
            "type": "person",
            "person": {"email": "user@awesome.com"},
        },
    }

    last_edited_by: pgp.PLastEditedBy = pgp.PLastEditedBy.from_dict(last_edited_by_args)

    assert last_edited_by.type == PropTypes.LAST_EDITED_BY
    assert last_edited_by.id == last_edited_by_args["id"]

    assert isinstance(last_edited_by.last_edited_by, Person)
    assert last_edited_by.last_edited_by.name == "guacs"
    assert last_edited_by.last_edited_by.id == "user-id"


def test_last_edited_time_fd():

    last_edited_time_args: dict[str, Any] = {
        "id": "I%40aJ",
        "type": "last_edited_time",
        "last_edited_time": "2022-12-23T08:50:00.000Z",
    }
    last_edited_time: pgp.PLastEditedTime = pgp.PLastEditedTime.from_dict(
        last_edited_time_args
    )

    assert last_edited_time.type == PropTypes.LAST_EDITED_TIME
    assert last_edited_time.id == last_edited_time_args["id"]

    assert last_edited_time.last_edited_time == datetime.fromisoformat(
        last_edited_time_args["last_edited_time"]
    )


def test_multi_select_fd():

    multi_select_args: dict[str, Any] = {
        "id": "%5BELZ",
        "type": "multi_select",
        "multi_select": [
            {
                "id": "427ef136-4bf2-46f7-bb05-3b4d8039cdb0",
                "name": "Optio Two",
                "color": "blue",
            },
            {
                "id": "40bc2943-ff3e-473c-a9eb-cc3268d043cb",
                "name": "Option Three",
                "color": "green",
            },
        ],
    }
    multi_select: pgp.PMultiselect = pgp.PMultiselect.from_dict(multi_select_args)

    assert multi_select.type == PropTypes.MULTI_SELECT
    assert multi_select.id == multi_select_args["id"]

    assert len(multi_select.options) == 2
    assert all((isinstance(opt, Option) for opt in multi_select.options))


def test_number_fd():

    number_args: dict[str, Any] = {"id": "sXRE", "type": "number", "number": 123}
    number: pgp.PNumber = pgp.PNumber.from_dict(number_args)

    assert number.type == PropTypes.NUMBER
    assert number.id == number_args["id"]

    assert number.number == 123


def test_number_empty_fd():

    number_args: dict[str, Any] = {"id": "sXRE", "type": "number", "number": None}
    number: pgp.PNumber = pgp.PNumber.from_dict(number_args)

    assert number.number is None


def test_people_fd():

    people_args: dict[str, Any] = {
        "id": "zk%5Ec",
        "type": "people",
        "people": [
            {
                "object": "user",
                "id": "user-id",
                "name": "guacs",
                "avatar_url": "www.some_url.com/image.jpg",
                "type": "person",
                "person": {"email": "guacs@awesome.com"},
            }
        ],
    }
    people: pgp.PPeople = pgp.PPeople.from_dict(people_args)

    assert people.type == PropTypes.PEOPLE
    assert people.id == people_args["id"]

    assert len(people.people) == 1
    assert isinstance(people.people[0], Person)


def test_phone_number_fd():

    phone_number_args: dict[str, Any] = {
        "id": "HZkg",
        "type": "phone_number",
        "phone_number": "1234567890",
    }
    phone_number: pgp.PPhonenumber = pgp.PPhonenumber.from_dict(phone_number_args)

    assert phone_number.type == PropTypes.PHONE_NUMBER
    assert phone_number.id == phone_number_args["id"]

    assert phone_number.phone_number == phone_number_args["phone_number"]


def test_phone_number_empty_fd():

    phone_number_args: dict[str, Any] = {
        "id": "HZkg",
        "type": "phone_number",
        "phone_number": None,
    }
    phone_number: pgp.PPhonenumber = pgp.PPhonenumber.from_dict(phone_number_args)

    assert phone_number.type == PropTypes.PHONE_NUMBER
    assert phone_number.id == phone_number_args["id"]

    assert phone_number.phone_number is None


def test_relation_fd():

    relation_args: dict[str, Any] = {
        "id": "mr%3Bm",
        "type": "relation",
        "relation": [{"id": "page-id"}],
        "has_more": False,
    }
    relation: pgp.PRelation = pgp.PRelation.from_dict(relation_args)

    assert relation.type == PropTypes.RELATION
    assert relation.id == relation_args["id"]

    assert relation.has_more is False
    assert relation.relations == ["page-id"]


def test_rollup_fd():

    rollup_args: dict[str, Any] = {
        "id": "omRg",
        "type": "rollup",
        "rollup": {"type": "number", "number": 0, "function": "checked"},
    }
    rollup: pgp.PRollup = pgp.PRollup.from_dict(rollup_args)

    assert rollup.type == PropTypes.ROLLUP
    assert rollup.id == rollup_args["id"]

    assert rollup.function == RollupFunctions.CHECKED
    assert rollup.value_type == "number"
    assert rollup.value == 0


def test_rich_text_fd():

    rich_text_args: dict[str, Any] = {
        "id": "eINr",
        "type": "rich_text",
        "rich_text": [
            {
                "type": "text",
                "text": {"content": "some text", "link": None},
                "annotations": {
                    "bold": False,
                    "italic": False,
                    "strikethrough": False,
                    "underline": False,
                    "code": False,
                    "color": "default",
                },
                "plain_text": "some text",
                "href": None,
            }
        ],
    }
    rich_text: pgp.PRichtext = pgp.PRichtext.from_dict(rich_text_args)

    assert rich_text.type == PropTypes.RICH_TEXT
    assert rich_text.id == rich_text_args["id"]

    assert rich_text.text == "some text"


def test_select_fd():

    select_args: dict[str, Any] = {
        "id": "JvoV",
        "type": "select",
        "select": {
            "id": "4c11e437-d154-47f5-ba12-d50e1ea19620",
            "name": "Option One",
            "color": "default",
        },
    }
    select: pgp.PSelect = pgp.PSelect.from_dict(select_args)

    assert select.type == PropTypes.SELECT
    assert select.id == select_args["id"]

    assert isinstance(select.option, Option)
    assert select.option.name == "Option One"
    assert select.option.color == Colors.DEFAULT


def test_select_empty_fd():

    select_args: dict[str, Any] = {"id": "JvoV", "type": "select", "select": None}
    select: pgp.PSelect = pgp.PSelect.from_dict(select_args)

    assert select.type == PropTypes.SELECT
    assert select.id == select_args["id"]

    assert select.option is None


def test_status_fd():

    status_args: dict[str, Any] = {
        "id": "XTsR",
        "type": "status",
        "status": {
            "id": "fa213733-dce4-4add-b952-2f482c4e0195",
            "name": "Not started",
            "color": "default",
        },
    }
    status: pgp.PStatus = pgp.PStatus.from_dict(status_args)

    assert status.type == PropTypes.STATUS
    assert status.id == status_args["id"]

    assert isinstance(status.status, Option)


def test_url_fd():

    url_args: dict[str, Any] = {"id": "QgOu", "type": "url", "url": "www.google.com"}
    url: pgp.PUrl = pgp.PUrl.from_dict(url_args)

    assert url.type == PropTypes.URL
    assert url.id == url_args["id"]

    assert url.url == "www.google.com"


def test_url_empty_fd():

    url_args: dict[str, Any] = {"id": "QgOu", "type": "url", "url": None}
    url: pgp.PUrl = pgp.PUrl.from_dict(url_args)

    assert url.url is None
