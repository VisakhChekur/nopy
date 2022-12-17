import json
from datetime import datetime
from datetime import timedelta
from pathlib import Path

import pytest

import nopy.properties.common_properties as cp
import nopy.properties.db_properties as dbp
from nopy import Database
from nopy.enums import NumberFormat
from nopy.objects.properties import Properties


@pytest.fixture
def props_with_id(options: list[cp.Option]):

    props = Properties()

    props.add(dbp.DBCheckbox("Checkbox", id="0"))
    props.add(dbp.DBCreatedBy("Created by", id="1"))
    props.add(dbp.DBCreatedTime("Created time", id="2"))
    props.add(dbp.DBDate("Date", id="3"))
    props.add(dbp.DBEmail("Email", id="4"))
    props.add(dbp.DBFiles("Files", id="5"))
    props.add(dbp.DBFormula("Formula", "add(1, 2)", id="6"))
    props.add(dbp.DBLastEditedBy("Last edited by", id="7"))
    props.add(dbp.DBLastEditedTime("Last edited time", id="8"))
    props.add(dbp.DBMultiSelect("Multi select", options[:2], id="9"))
    props.add(dbp.DBNumber("Number", NumberFormat.RUPEE, id="10"))
    props.add(dbp.DBPhoneNumber("Phone", id="11"))
    props.add(dbp.DBSelect("Select", options[2:4], id="12"))
    props.add(dbp.DBText("Text", id="13"))
    props.add(dbp.DBUrl("Url", id="14"))
    props.add(dbp.DBTitle("Title", id="title"))

    return props


@pytest.fixture
def props_without_id(options: list[cp.Option]):

    props = Properties()

    props.add(dbp.DBCheckbox("Checkbox"))
    props.add(dbp.DBCreatedBy("Created by"))
    props.add(dbp.DBCreatedTime("Created time"))
    props.add(dbp.DBDate("Date"))
    props.add(dbp.DBEmail("Email"))
    props.add(dbp.DBFiles("Files"))
    props.add(dbp.DBFormula("Formula", "add(1, 2)"))
    props.add(dbp.DBLastEditedBy("Last edited by"))
    props.add(dbp.DBLastEditedTime("Last edited time"))
    props.add(dbp.DBMultiSelect("Multi select", options[:2]))
    props.add(dbp.DBNumber("Number", NumberFormat.RUPEE))
    props.add(dbp.DBPhoneNumber("Phone"))
    props.add(dbp.DBSelect("Select", options[2:4]))
    props.add(dbp.DBText("Text"))
    props.add(dbp.DBUrl("Url"))
    props.add(dbp.DBTitle("Title"))

    return props


@pytest.fixture
def props_with_id_serialized(test_data_fp: Path):
    """This returns the expected serialized dictionary
    for the properties as defined above."""

    with open(test_data_fp / "serialized_dbs/prop-with-id.json", "r") as f:
        return json.load(f)


@pytest.fixture
def db(rich_text_list: list[cp.Text], props: Properties):
    created_time = datetime.now()
    last_edited_time = datetime.now() + timedelta(2)

    return Database(
        rich_title=rich_text_list,
        created_time=created_time,
        last_edited_time=last_edited_time,
        rich_description=rich_text_list,
        icon=cp.Emoji("some emoji"),
        cover=cp.File("some url"),
        parent=cp.PageParent("page-id"),
        url="db-url",
        is_inline=False,
        id="db-id",
        archived=False,
        properties=props,
    )
