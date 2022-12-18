import socket
from pathlib import Path
from typing import Any

import pytest
from dotenv import load_dotenv  # type: ignore

from nopy.client import NotionClient

ENV_PATH = Path(__file__).parent / "../.env"
load_dotenv(ENV_PATH)


# Disabling network access
def block_network(*args: Any):
    raise Exception("no network access allowed")


socket.socket = block_network


# ----- FIXTURES -----
@pytest.fixture(scope="session")
def client():

    return NotionClient()
