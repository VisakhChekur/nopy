import pytest
import json
from pathlib import Path
from notion.client import NotionClient
from notion.mapper import Mapper
from dotenv import load_dotenv

# ----- CONFIGURING PYTEST -----
def pytest_addoption(parser: pytest.Parser):
    parser.addoption(
        "--runapi",
        action="store_true",
        default=False,
        help="run tests that call the Notion API",
    )


def pytest_configure(config: pytest.Config):
    config.addinivalue_line("markers", "serialize: mark test serialization test")
    config.addinivalue_line("markers", "api: mark tests calling Notion API")


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]):
    # Setting up the configs so that test marked with 'api' is only
    # run if explicitly specified.
    if config.getoption("--runapi"):
        return

    skip_api = pytest.mark.skip(reason="need --runapi option to run")
    for item in items:
        if "api" in item.keywords:
            item.add_marker(skip_api)

# ----- MISCELLANEOUS -----


# ----- FIXTURES -----
@pytest.fixture(scope="session")
def client():
    load_dotenv()
    return NotionClient()

@pytest.fixture(scope="session")
def mapper(client):

    return Mapper(client)

@pytest.fixture
def db_dict():
    sample_db_file = Path(__file__).parent / "samples/db.json"
    with open(sample_db_file, "r") as f:
        return json.load(f)
