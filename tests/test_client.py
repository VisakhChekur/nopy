import os

import pytest

from nopy.client import NotionClient
from nopy.errors import TokenNotFoundError


def test_client_without_token():

    os.environ.pop("NOTION_TOKEN", None)
    with pytest.raises(TokenNotFoundError):

        NotionClient()
