import pytest

import nopy.properties.db_properties as dbp
from nopy.objects.properties import Properties


@pytest.fixture
def text():

    return dbp.DBText("Text prop", id="1")


@pytest.fixture
def email():

    return dbp.DBEmail("Email prop", id="2")


@pytest.fixture
def checkbox():

    return dbp.DBCheckbox("Checkbox")


@pytest.fixture
def props(text, email):

    props = Properties()
    for prop in (text, email):
        props.add_prop(prop)
    return props


def test_add_prop(text):

    props = Properties()
    props.add_prop(text)

    assert text.id in props
    assert text.id in props._ids
    assert text.name in props._names


def test_get_prop(props):

    # Testing with name
    text = props["Text prop"]
    assert isinstance(text, dbp.DBText)
    assert text.name == "Text prop"

    # Testing with id
    text = props["1"]
    assert isinstance(text, dbp.DBText)
    assert text.name == "Text prop"


def test_pop_prop(props: Properties):

    # Deleting with prop name
    text = props.pop("Text prop")
    assert text.name not in props
    assert text.id not in props
    assert text.name not in props._names
    assert text.id not in props._ids

    email = props.pop("2")
    assert email.name not in props
    assert email.id not in props
    assert email.name not in props._names
    assert email.id not in props._ids


def test_update_prop_name(
    props: Properties, checkbox: dbp.DBCheckbox, text: dbp.DBText
):

    # 'text' is the one being replaced
    props.update_prop(text.name, checkbox)

    assert text.name not in props
    assert text.id in props
    assert checkbox.name in props
    assert isinstance(props[text.id], dbp.DBCheckbox)


def test_update_prop_id(props: Properties, text: dbp.DBText, checkbox: dbp.DBCheckbox):

    props.update_prop(text.id, checkbox)

    assert text.name not in props
    assert text.id in props
    assert checkbox.name in props
    assert isinstance(props[text.id], dbp.DBCheckbox)
