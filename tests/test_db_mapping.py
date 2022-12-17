import json
from pathlib import Path
from typing import Any

from nopy import Database
from nopy.client import NotionClient
from nopy.mappers import map_to_db
from nopy.objects.properties import Properties
from nopy.properties import common_properties as cp
from nopy.properties import db_properties as dbp


def get_db(fp: Path, client: NotionClient) -> Database:

    with open(fp, "r") as f:
        data: dict[str, Any] = json.load(f)
        return map_to_db(data, client)


def test_db_full(test_data_fp: Path, client: NotionClient):

    db = get_db(test_data_fp / "db-full.json", client)

    assert isinstance(db, Database)
    assert db.id == "db-id"
    assert all(isinstance(rt, cp.Text) for rt in db.rich_title)
    assert db.title == "Created DB"
    assert all(isinstance(rt, cp.Text) for rt in db.rich_description)
    assert db.description == "Created with nopy"
    assert db.is_inline
    assert db.url == "https://www.example.com"
    assert not db.archived
    assert isinstance(db.icon, cp.Emoji)


def test_db_properties(test_data_fp: Path, client: NotionClient):

    db = get_db(test_data_fp / "db-full.json", client)

    expected = {
        "Created DB": dbp.DBTitle,
        "Number": dbp.DBNumber,
        "Phone": dbp.DBPhoneNumber,
        "Created time": dbp.DBCreatedTime,
        "Status": dbp.DBStatus,
        "Files & media": dbp.DBFiles,
        "Date": dbp.DBDate,
        "Formula": dbp.DBFormula,
        "Select": dbp.DBSelect,
        "Last edited time": dbp.DBLastEditedTime,
        "Text": dbp.DBText,
        "Checkbox": dbp.DBCheckbox,
        "Email": dbp.DBEmail,
        "URL": dbp.DBUrl,
        "Multi-select": dbp.DBMultiSelect,
    }

    assert isinstance(db.properties, Properties)
    for name, prop_type in expected.items():
        assert name in db.properties
        assert isinstance(db.properties[name], prop_type)


def test_db_no_cover(test_data_fp: Path, client: NotionClient):

    db = get_db(test_data_fp / "db-no-cover.json", client)

    assert db.cover is None


def test_db_no_icon(test_data_fp: Path, client: NotionClient):

    db = get_db(test_data_fp / "db-no-icon.json", client)

    assert db.icon is None


def test_db_no_title(test_data_fp: Path, client: NotionClient):

    db = get_db(test_data_fp / "db-empty-title.json", client)

    assert isinstance(db.rich_title, list)
    assert len(db.rich_title) == 0
    assert db.title == ""
