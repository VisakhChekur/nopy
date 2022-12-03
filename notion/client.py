import os
from typing import Any
from typing import Callable

import requests

from notion.constants import API_VERSION
from notion.constants import BLOCK_ENDPOINT
from notion.constants import DB_ENDPOINT
from notion.constants import PAGE_ENDPOINT
from notion.exceptions import AuthenticationError
from notion.exceptions import NotFoundError


def _handle_http_error(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to handle HTTPErrors."""

    def wrapper(*args: Any, **kwargs: Any) -> Any:

        try:
            return func(*args, **kwargs)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise AuthenticationError("Invalid Notion token")
            if e.response.status_code == 404:
                raise NotFoundError(
                    "Invalid 'id' for the requested resource or this integration hasn't been given access."
                )
            raise e

    return wrapper


class NotionClient:
    """A client to connect with Notion using the official Notion API."""

    def __init__(self, token: str = ""):
        """Constructor for client.

        Args:
            token:
                The Notion token from the Notion integration. If it's not
                provided, then the value must be present in the environment
                variables with the name `NOTION_TOKEN`. Refer the following:
                https://developers.notion.com/docs/create-a-notion-integration

        Raises:
            AuthenticationError: Token not found.
        """

        try:
            self._token = token or os.environ["NOTION_TOKEN"]
        except KeyError:
            raise AuthenticationError(
                "Token not provided and not found from environment variables with the name `NOTION_TOKEN`"
            )

        # The headers that are included in every request sent to
        # Notion.
        self._headers = {
            "Authorization": f"Bearer {self._token}",
            "Notion-Version": API_VERSION,
        }

    # ----- DATABASE RELATED METHODS ------
    def retrieve_db(self, db_id: str):
        """Retrives the database from Notion.

        Args:
            db_id:
                The id of the database.

        Returns:
            The database.

        Raises:
            AuthenticationError:
                Invalid Notion token
            NotFoundError:
                Database not found.
            HTTPError:
                Any error that took place when making requests to Notion.
        """

        db_dict = self._get_request(DB_ENDPOINT + db_id)
        return db_dict

    # ------ PAGE RELATED METHODS -----
    def retrieve_page(self, page_id: str):
        """Retrieves the page from Notion.

        Args:
            page_id:
                The id of the page.

        Returns:
            The page.

        Raises:
            AuthenticationError:
                Invalid Notion token
            NotFoundError:
                Database not found.
            HTTPError:
                Any error that took place when making requests to Notion.

        """

        page_dict = self._get_request(PAGE_ENDPOINT + page_id)
        return page_dict

    # ----- BLOCK RELATED METHODS -----
    def retrieve_bloc(self, block_id: str):
        """Retrieves the page from Notion.

        Args:
            block_id:
                The id of the block.

        Returns:
            The block.

        Raises:
            AuthenticationError:
                Invalid Notion token
            NotFoundError:
                Database not found.
            HTTPError:
                Any error that took place when making requests to Notion.

        """

        block_dict = self._get_request(BLOCK_ENDPOINT + block_id)
        return block_dict

    # ------ PRIVATE METHODS ------

    @_handle_http_error
    def _get_request(self, endpoint: str):

        response = requests.get(endpoint, headers=self._headers)
        response.raise_for_status()
        return response.json()
