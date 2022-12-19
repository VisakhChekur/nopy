import json
import socket
from pathlib import Path
from typing import Any

import pytest
from dotenv import load_dotenv  # type: ignore

from nopy.client import NotionClient

ENV_PATH = Path(__file__).parent / "../.env"
load_dotenv(ENV_PATH)

DATA_DIR = Path(__file__).parent / "data"


# Disabling network access
def block_network(*args: Any):
    raise Exception("no network access allowed")


socket.socket = block_network


# ----- FIXTURES -----
@pytest.fixture(scope="session")
def client():

    client = NotionClient()
    yield client
    client.close()


@pytest.fixture
def full_db():

    fp = DATA_DIR / "test_database" / "full_db.json"
    with open(fp, "r") as f:
        return json.load(f)
