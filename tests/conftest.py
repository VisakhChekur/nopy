from pathlib import Path

import pytest

import nopy.properties.common_properties as cp
from nopy.client import NotionClient
from nopy.enums import Colors


@pytest.fixture(scope="session")
def test_data_fp():

    return Path(__file__).parent / "test-data"


@pytest.fixture(scope="session")
def client():
    return NotionClient("secret-token")


@pytest.fixture
def options():

    return [cp.Option(f"Option {str(i)}", str(i), Colors.BLUE) for i in range(5)]


@pytest.fixture
def rich_text_list():

    one = cp.Text("A text")
    two = cp.Text("with", annotations=cp.Annotations(bold=True))
    three = cp.Text("styling", annotations=cp.Annotations(code=True, color=Colors.RED))
    return [one, two, three]
