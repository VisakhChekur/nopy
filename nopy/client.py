import json
import os
from functools import wraps
from pathlib import Path
from pprint import pprint
from typing import Any
from typing import Callable
from typing import Optional
from typing import Union

import requests
from requests.adapters import HTTPAdapter
from requests.adapters import Retry

from .constants import API_VERSION
from .constants import BLOCK_ENDPOINT
from .constants import DB_ENDPOINT
from .constants import PAGE_ENDPOINT
from .constants import QUERY_ENDPOINT
from .exceptions import AuthenticationError
from .exceptions import FormatError
from .exceptions import NotFoundError
from .exceptions import NotionAPIError
from .exceptions import NotionError
from .mappers import map_to_db
from .mappers import map_to_page
from .objects.db import Database
from .objects.page import Page


# TODO: Try 'faster-than-requests' instead of 'requests'
def _handle_http_error(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to handle errors during API calls."""

    @wraps(func)
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
            if e.response.status_code == 400:
                raise FormatError(e.response.json())
            raise NotionAPIError(e.response.json())
        except Exception as e:
            raise NotionError(e)

    return wrapper


class NotionClient:
    """A client to connect with Notion using the official Notion API.
    Args:
        token:
            The Notion token from the Notion integration. If it's not
            provided, then the value must be present in the environment
            variables with the name `NOTION_TOKEN`. For more details, refer
            the following:
            https://developers.notion.com/docs/create-a-notion-integration

        retry:
            If provided, retries will be done on requests that fail due to
            issues such as network issues. If a dictionary is provided, the
            keys and values must match the allowed values in the `Retry`
            constructor. An instance of a `Retry` object can be provided which
            can be from `requests.adapter` or from `urllib3.util`. For more
            details, refer the following:
            https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#urllib3.util.Retry

    Raises:
        AuthenticationError: Token not found.
    """

    def __init__(
        self, token: str = "", *, retry: Optional[Union[dict[str, Any], Retry]] = None
    ):

        try:
            self._token = token or os.environ["NOTION_TOKEN"]
        except KeyError:
            raise AuthenticationError(
                "Token not provided and not found from environment variables with the name `NOTION_TOKEN`"
            )

        self._db_cache: dict[str, Database] = {}

        self._retry = retry
        self._request_session = self._get_request_session()
        # The headers that are included in every request sent to
        # Notion.
        self._headers = {
            "Authorization": f"Bearer {self._token}",
            "Notion-Version": API_VERSION,
        }

    # ----- DATABASE RELATED METHODS ------
    def retrieve_db(
        self, db_id: str, use_cached: bool = True, *, save_to_fp: str | Path = ""
    ) -> Database:
        """Retrives the database from Notion

        Returns an instance of `Database`.

        Args:
            db_id:
                The id of the database to retrieve.

            use_cached:
                If 'True', then the cached database is returned, if available.

            save_to_fp:
                If provided, saves the returned response JSON from Notion
                to the provided file path.

        Returns:
            The database.

        Raises:
            AuthenticationError: Invalid Notion token
            NotFoundError: Database not found.
            NotionAPIError: Any error that took place when making requests to
            Notion.
        """

        cached_db: Optional[Database] = self._db_cache.get(db_id, None)
        if use_cached and cached_db:
            return cached_db

        db_dict = self._get_request(DB_ENDPOINT + db_id)
        if save_to_fp:
            self._save_to_fp(db_dict, Path(save_to_fp))

        db = map_to_db(db_dict, self)
        self._db_cache[db.id] = db

        return db

    def retrieve_db_raw(self, db_id: str) -> dict[str, Any]:
        """Retrieves a database from Notion.

        Returns the database as the raw dictionary as returned by Notion.

        Args:
            db_id (str): The id of the database to retrieve.

        Returns:
            The raw dictionary as returned by Notion.

        Raises:
            AuthenticationError: Invalid Notion token
            NotFoundError: Database not found.
            NotionAPIError: Any error that took place when making requests to
            Notion.

        """
        return self._get_request(DB_ENDPOINT + db_id)

    def create_db(self, db_dict: dict[str, Any]) -> None:
        """Creates a database.

        Args:
            db_dict (dict[str, Any]):
                The details of the database to be created in a format that
                adheres to the Notion specifications.

        Raises:
            AuthenticationError: Invalid Notion token
            FormatError: Invalid format for `db_dict`.
            NotionAPIError: Any error that took place when making requests
            to Notion.

        """
        self._post_request(DB_ENDPOINT, db_dict)

    def update_db(self, db_id: str, db_dict: dict[str, Any]) -> None:
        """Updates the database.

        Args:
            db_dict (dict[str, Any]):
                The details of the database to be updated in a format that
                adheres to the Notion specifications.

        Raises:
            AuthenticationError: Invalid Notion token.
            FormatError: Invalid format for `db_dict`.
            NotionAPIError: Any error that took place when making requests to
            Notion.
        """
        endpoint = DB_ENDPOINT + db_id
        resp = self._patch_request(endpoint, db_dict)
        pprint(resp)

    def query_db(self, db_id: str, query_dict: dict[str, Any]) -> list[Page]:
        """Qeuries the database.

        Args:
            db_id (str): The id of the database to query.
            query_dict (dict[str, Any]):
                The filters and the sort conditions in a format that
                adheres to the Notion specifications.

        Returns:
            A list of `Page` instances that satisfy the query conditions.

        Raises:
            AuthenticationError: Invalid Notion token
            NotFoundError: Database not found.
            FormatError: Invalid format for `query_dict`.
            NotionAPIError: Any error that took place when making requests to
            Notion.

        """
        endpoint = QUERY_ENDPOINT.format(db_id)
        resp = self._post_request(endpoint, query_dict)

        db = self.retrieve_db(db_id)
        return [map_to_page(p, db, self) for p in resp["results"]]

    def query_db_raw(self, db_id: str, query_dict: dict[str, Any]) -> dict[str, Any]:
        """Qeuries the database.

        Args:
            db_id (str): The id of the database to query.
            query_dict (dict[str, Any]):
                The filters and the sort conditions in a format that
                adheres to the Notion specifications.

        Returns:
            The raw dictionary response as given by Notion.

        Raises:
            AuthenticationError: Invalid Notion token
            NotFoundError: Database not found.
            FormatError: Invalid format for `query_dict`.
            NotionAPIError: Any error that took place when making requests to
            Notion.

        """
        endpoint = QUERY_ENDPOINT.format(db_id)
        return self._post_request(endpoint, query_dict)

    # ------ PAGE RELATED METHODS -----
    def retrieve_page(self, page_id: str, *, save_to_fp: str | Path = ""):
        """Retrieves the page from Notion.

        Args:
            page_id:
                The id of the page.

        Returns:
            An instance of `Page`.

        Raises:
            AuthenticationError: Valid Notion token
            NotFoundError: Page not found.
            NotionAPIError: Any error that took place when making requests to
            Notion.

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

        return map_to_page(page_dict, db, self)

    def retrieve_page_raw(self, page_id: str) -> dict[str, Any]:
        """Retrieves the page from Notion.

        Args:
            page_id:
                The id of the page.

        Returns:
            The page as the raw dictionary as returned by Notion.

        Raises:
            AuthenticationError: Invalid Notion token
            NotFoundError: Page not found.
            NotionAPIError: Any error that took place when making requests to
            Notion.

        """
        return self._get_request(PAGE_ENDPOINT + page_id)

    # ----- BLOCK RELATED METHODS -----
    def retrieve_block(self, block_id: str, *, save_to_fp: str | Path = ""):
        """Retrieves the block from Notion.

        Args:
            block_id:
                The id of the block.

        Returns:
            The block.

        Raises:
            AuthenticationError: Invalid Notion token
            NotFoundError: Block not found.
            NotionAPIError: Any error that took place when making requests to
            Notion.

        """

        block_dict = self._get_request(BLOCK_ENDPOINT + block_id)
        if save_to_fp:
            self._save_to_fp(block_dict, Path(save_to_fp))

        return block_dict

    # ------ PRIVATE METHODS ------

    def _get_request_session(self):

        session = requests.Session()

        if not self._retry:
            return session

        if isinstance(self._retry, dict):
            retry = Retry(**self._retry)
        else:
            retry = self._retry

        session.mount("https://", HTTPAdapter(max_retries=retry))
        return session

    @staticmethod
    def _save_to_fp(data: dict[str, Any], fp: Path):
        """Saves the given data as JSON to the given file."""

        with open(fp, "w+") as f:
            json.dump(data, f, indent=4)

    @_handle_http_error
    def _get_request(self, endpoint: str):

        response = self._request_session.get(endpoint, headers=self._headers)
        response.raise_for_status()
        return response.json()

    @_handle_http_error
    def _post_request(self, endpoint: str, data: dict[str, Any]):

        response = self._request_session.post(
            endpoint, json=data, headers=self._headers
        )
        response.raise_for_status()
        return response.json()

    @_handle_http_error
    def _patch_request(self, endpoint: str, data: dict[str, Any]):

        response = self._request_session.patch(
            endpoint, json=data, headers=self._headers
        )
        response.raise_for_status()
        return response.json()
