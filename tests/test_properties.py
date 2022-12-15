import pytest

import nopy.properties.db_properties as dbp
from nopy.exceptions import PropertyExistsError
from nopy.exceptions import PropertyNotFoundError
from nopy.objects.properties import Properties


@pytest.fixture
def text():

    return dbp.DBText("Text prop", id="1")


@pytest.fixture
def props():

    return Properties()


def test_add_props(props, text):

    props.add(text)

    assert props._names[text.name] == text
    assert props._ids[text.id] == text
    assert text in props


def test_adding_same_prop(props, text):

    props.add(text)
    with pytest.raises(PropertyExistsError):
        props.add(text)


def test_adding_prop_with_same_name(props, text):

    props.add(text)
    with pytest.raises(PropertyExistsError):
        props.add(dbp.DBCheckbox(text.name))


def test_adding_prop_with_same_id(props, text):

    props.add(text)
    with pytest.raises(PropertyExistsError):
        props.add(dbp.DBCheckbox("Check", id=text.id))


def test_contains(props, text):

    props.add(text)
    assert text in props
    assert text.name in props
    assert text.id in props


def test_pop_with_name(props, text):

    props.add(text)
    assert props.pop(text.name) == text


def test_pop_with_id(props, text):

    props.add(text)
    assert props.pop(text.id) == text


def test_get_prop(props, text):

    props.add(text)
    assert props[text.name] == text
    assert props[text.id] == text


def test_invalid_prop_pop(props):

    with pytest.raises(PropertyNotFoundError):
        props.pop("invalid")
