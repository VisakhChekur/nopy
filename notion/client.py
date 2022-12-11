import json
import os
from pathlib import Path
from pprint import pprint
from typing import Any
from typing import Callable
from typing import Optional

import requests

from notion.constants import API_VERSION
from notion.constants import BLOCK_ENDPOINT
from notion.constants import DB_ENDPOINT
from notion.constants import PAGE_ENDPOINT
from notion.constants import QUERY_ENDPOINT
from notion.exceptions import AuthenticationError
from notion.exceptions import NotFoundError
from notion.exceptions import ValidationError
from notion.mapper import Mapper
from notion.objects.db import Database
from notion.objects.page import Page


# TODO: Try 'faster-than-requests' instead of 'requests'
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
        self._db_cache: dict[str, Database] = {}

    # ----- DATABASE RELATED METHODS ------
    def retrieve_db(
        self, db_id: str, use_cached: bool = True, *, save_to_fp: str | Path = ""
    ) -> Database:
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

        cached_db: Optional[Database] = self._db_cache.get(db_id, None)

        if use_cached and cached_db:
            return cached_db
        db_dict = self._get_request(DB_ENDPOINT + db_id)
        if save_to_fp:
            self._save_to_fp(db_dict, Path(save_to_fp))

        db = self._mapper.map_to_db(db_dict)
        self._db_cache[db.id] = db

        return db

    def retrieve_db_raw(self, db_id: str) -> dict[str, Any]:

        return self._get_request(DB_ENDPOINT + db_id)

    def create_db(self, db_dict: dict[str, Any]):

        self._post_request(DB_ENDPOINT, db_dict)

    def update_db(self, db_id: str, db_dict: dict[str, Any]):

        endpoint = DB_ENDPOINT + db_id
        resp = self._patch_request(endpoint, db_dict)
        pprint(resp)

    def query_db(self, db_id: str, query_dict: dict[str, Any]) -> list[Page]:

        endpoint = QUERY_ENDPOINT.format(db_id)
        resp = self._post_request(endpoint, query_dict)

        db = self.retrieve_db(db_id)
        return [self._mapper.map_to_page(p, db) for p in resp["results"]]

    def query_db_raw(self, db_id: str, query_dict: dict[str, Any]) -> dict[str, Any]:

        endpoint = QUERY_ENDPOINT.format(db_id)
        return self._post_request(endpoint, query_dict)

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

        # This is required to find the property names of a page if the
        # page's parent is a dictionary. Pages that are not children of
        # databases, have no properties except 'title'.
        db: Optional[Database] = None
        if page_dict["parent"]["type"] == "database_id":
            db = self.retrieve_db(page_dict["parent"]["database_id"])

        return self._mapper.map_to_page(page_dict, db)

    def retrieve_page_raw(self, page_id: str) -> dict[str, Any]:

        return self._get_request(PAGE_ENDPOINT + page_id)

    # ----- BLOCK RELATED METHODS -----
    def retrieve_block(self, block_id: str, *, save_to_fp: str | Path = ""):
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

    @_handle_http_error
    def _patch_request(self, endpoint: str, data: dict[str, Any]):

        response = requests.patch(endpoint, json=data, headers=self._headers)
        response.raise_for_status()
        return response.json()
