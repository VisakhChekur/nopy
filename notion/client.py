import json
import os
from pathlib import Path
from typing import Any
from typing import Callable

import requests

from notion.constants import API_VERSION
from notion.constants import BLOCK_ENDPOINT
from notion.constants import DB_ENDPOINT
from notion.constants import PAGE_ENDPOINT
from notion.exceptions import AuthenticationError
from notion.exceptions import NotFoundError
from notion.exceptions import ValidationError
from notion.mapper import Mapper


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
            raise ValidationError(e.response.json())

    return wrapper


class NotionClient:
    """A client to connect with Notion using the official Notion API.
    Args:
        token:
            The Notion token from the Notion integration. If it's not
            provided, then the value must be present in the environment
            variables with the name `NOTION_TOKEN`. Refer the following:
            https://developers.notion.com/docs/create-a-notion-integration

    Raises:
        AuthenticationError: Token not found.
    """

    def __init__(self, token: str = ""):
        """Constructor for client."""

        try:
            self._token = token or os.environ["NOTION_TOKEN"]
        except KeyError:
            raise AuthenticationError(
                "Token not provided and not found from environment variables with the name `NOTION_TOKEN`"
            )

        self._mapper = Mapper(self)
        # The headers that are included in every request sent to
        # Notion.
        self._headers = {
            "Authorization": f"Bearer {self._token}",
            "Notion-Version": API_VERSION,
        }

    # ----- DATABASE RELATED METHODS ------
    def retrieve_db(self, db_id: str, *, save_to_fp: str | Path = ""):
        """Retrives the database from Notion.

        Args:
            db_id:
                The id of the database.

            save_to_fp:
                If provided, saves the returned response JSON from Notion
                to the provided file path.

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
        if save_to_fp:
            self._save_to_fp(db_dict, Path(save_to_fp))

        return self._mapper.map_to_db(db_dict)

    def create_db(self, db_dict: dict[str, Any]):

        self._post_request(DB_ENDPOINT[:-1], db_dict)

    # ------ PAGE RELATED METHODS -----
    def retrieve_page(self, page_id: str, *, save_to_fp: str | Path = ""):
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
        if save_to_fp:
            self._save_to_fp(page_dict, Path(save_to_fp))

        return page_dict

    # ----- BLOCK RELATED METHODS -----
    def retrieve_bloc(self, block_id: str, *, save_to_fp: str | Path = ""):
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
        if save_to_fp:
            self._save_to_fp(block_dict, Path(save_to_fp))

        return block_dict

    # ------ PRIVATE METHODS ------

    @staticmethod
    def _save_to_fp(data: dict[str, Any], fp: Path):
        """Saves the given data as JSON to the given file."""

        with open(fp, "w+") as f:
            json.dump(data, f, indent=4)

    @_handle_http_error
    def _get_request(self, endpoint: str):

        response = requests.get(endpoint, headers=self._headers)
        response.raise_for_status()
        return response.json()

    @_handle_http_error
    def _post_request(self, endpoint: str, data: dict[str, Any]):

        response = requests.post(endpoint, json=data, headers=self._headers)
        response.raise_for_status()
        return response.json()
