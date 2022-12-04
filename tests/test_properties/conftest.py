import json
from pathlib import Path
from typing import Any

import pytest


@pytest.fixture(scope="session")
def db():

    sample_db_file = Path(__file__).parent / "../samples/db.json"
    with open(sample_db_file, "r") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def props(db: dict[str, Any]):

    return db["properties"]


@pytest.fixture(scope="session")
def option(props):

    return props["Select"]["select"]["options"][0]


@pytest.fixture(scope="session")
def group(props):

    return props["Status"]["status"]["groups"][0]
