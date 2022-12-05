import dateutil.parser as date_parser

from notion.client import NotionClient
from notion.properties.common_properties import Text
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
from notion.properties.db_properties import DBProp
from notion.properties.db_properties import DBSelect
from notion.properties.db_properties import DBStatus
from notion.properties.db_properties import DBText
from notion.properties.db_properties import DBTitle
from notion.properties.db_properties import DBUrl


def test_map_to_db(mapper, db_dict):

    db = mapper.map_to_db(db_dict)

    assert db.title == "Test Database"
    assert db.created_time == date_parser.parse("2022-12-03T04:17:00.000Z")
    assert db.last_edited_time == date_parser.parse("2022-12-04T18:59:00.000Z")
    assert db.description == "Some description"
    assert db.icon.emoji == "🌎"
    assert db.url == "https://www.notion.so/test_db"
    assert db.archived == False  # noqa
    assert db.is_inline == True  # noqa
    assert db.id == "test_db_id"
    assert db.cover.url == "cover_url"
    assert db.parent.id == "test_page_id"
    assert isinstance(db._client, NotionClient)
    assert all((isinstance(rt, Text) for rt in db.rich_title))
    assert all((isinstance(rt, Text) for rt in db.rich_title))


def test_mapped_db_props(mapper, db_dict):

    props = mapper.map_to_db(db_dict).properties

    # Unsupported = people,
    expected_props = {
        "Formula": DBFormula,
        "Email": DBEmail,
        "Created by": DBCreatedBy,
        "Created time": DBCreatedTime,
        "Last edited time": DBLastEditedTime,
        "Select": DBSelect,
        "Phone": DBPhoneNumber,
        "Multi-select": DBMultiSelect,
        "URL": DBUrl,
        "Text": DBText,
        "Files & media": DBFiles,
        "Number": DBNumber,
        "Checkbox": DBCheckbox,
        "Date": DBDate,
        "Last edited by": DBLastEditedBy,
        "Status": DBStatus,
        "Name": DBTitle,
        "Person": DBProp,
    }
    for prop_name, prop_type in expected_props.items():
        assert prop_name in props
        assert isinstance(props[prop_name], prop_type)
