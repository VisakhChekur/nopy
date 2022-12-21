# pyright: reportPrivateUsage=false

import pytest

from nopy import Properties
from nopy.errors import PropertyExistsError
from nopy.errors import PropertyNotFoundError
from nopy.props import DBText

# ----- Fixtures -----


@pytest.fixture(scope="module")
def prop() -> DBText:

    return DBText(id="1", name="text")


@pytest.fixture(scope="module")
def prop_no_id() -> DBText:

    return DBText(name="text")


@pytest.fixture(scope="module")
def prop_no_name() -> DBText:

    return DBText(id="1")


@pytest.fixture
def props() -> Properties:

    return Properties()


# ----- Tests -----


def test_add(props: Properties, prop: DBText):

    props.add(prop)

    assert prop in props._props
    assert prop.name in props._names
    assert prop.id in props._ids


def test_add_prop_no_name(props: Properties, prop_no_name: DBText):

    with pytest.raises(ValueError):
        props.add(prop_no_name)


def test_add_same_prop(props: Properties, prop: DBText):

    props.add(prop)
    with pytest.raises(PropertyExistsError):
        props.add(prop)


def test_add_prop_same_name(props: Properties, prop: DBText):

    props.add(prop)
    same_name_prop = DBText(name=prop.name)
    with pytest.raises(PropertyExistsError):
        props.add(same_name_prop)


def test_get_with_name(props: Properties, prop: DBText):

    props.add(prop)
    assert props[prop.name] is prop


def test_get_with_id(props: Properties, prop: DBText):

    props.add(prop)
    assert props[prop.id] is prop


def test_get_invalid_identifier(props: Properties):

    with pytest.raises(PropertyNotFoundError):
        props["invalid identifier"]


def test_pop_with_prop(props: Properties, prop: DBText):

    props.add(prop)
    assert props.pop(prop) is prop


def test_pop_with_name(props: Properties, prop: DBText):

    props.add(prop)
    assert props.pop(prop.name) is prop


def test_pop_with_id(props: Properties, prop: DBText):

    props.add(prop)
    assert props.pop(prop.id) is prop


def test_pop_invalid_name(props: Properties):

    with pytest.raises(PropertyNotFoundError):
        props.pop("invalid")


def test_pop_invalid_prop(props: Properties, prop: DBText):

    with pytest.raises(PropertyNotFoundError):
        props.pop(prop)
