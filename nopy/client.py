import logging
import os
from dataclasses import dataclass
from functools import lru_cache
from json import JSONDecodeError
from types import TracebackType
from typing import Any
from typing import Literal
from typing import Optional
from typing import Type
from typing import Union

import httpx

from nopy.constants import API_BASE_URL
from nopy.constants import API_VERSION
from nopy.constants import APIEndpoints
from nopy.errors import APIResponseError
from nopy.errors import HTTPError
from nopy.errors import TokenNotFoundError
from nopy.objects import Block
from nopy.objects import Comment
from nopy.objects import Database
from nopy.objects import Page
from nopy.objects import User
from nopy.utils import make_logger


@dataclass
class ClientConfig:
    """Configuration options for the `Client`.

    Attributes:
        base_url: The base url.
        api_version: The version of the Notion API.
        timeout:
            The number of seconds to wait before raising an error.
        retries:
            The number of retries to make before raising an error.
        log_level: The level of the logging.
        logger: The logger to use when logging.
    """

    base_url: str = API_BASE_URL
    api_version: str = API_VERSION
    timeout: int = 5
    retries: int = 0
    log_level: int = logging.WARNING
    logger: Optional[logging.Logger] = None


class NotionClient:
    """The client that can be used to interact with the Notion API."""

    def __init__(
        self,
        token: str = "",
        config: Optional[Union[dict[str, Any], ClientConfig]] = None,
    ):
        """Constructor for `NotionClient`.

        Args:
            token:
                The Notion integration token. If it's not provided,
                then the token is looked for in the environment variables
                with the name 'NOTION_TOKEN'.
            config:
                The options to use to configure the client with. If not
                provided, then the base configurations are used.

        Raises:
            AuthenticationError:
                Raised if the Notion token wasn't provided and it wasn't
                found from the environment variables.
        """

        try:
            self.token = token or os.environ["NOTION_TOKEN"]
        except KeyError:
            msg = "token not provided and not found with key 'NOTION_TOKEN' from the environment variables"
            raise TokenNotFoundError(msg)

        if isinstance(config, dict):
            self._config = ClientConfig(**config)
        else:
            self._config = config or ClientConfig()

        self._client: httpx.Client = self._get_client()
        self._logger: logging.Logger = self._get_logger()

    # ------ Database related endpoints ------

    def retrieve_db(self, db_id: str, use_cache: bool = True) -> Database:
        """Retreives the database.

        Attributes:
            db_id: The id of the database to retrieve.

        Returns:
            The database.

        Raises:
            APIResponseError:
                Raised when the Notion API returns a status code that's not 2xx.
            HTTPError:
                Raised when there's some error when making the API call.
        """

        db_dict = self.retrieve_db_raw(db_id, use_cache)
        self._logger.info(" Mapping response to a Database instance")
        return Database.from_dict(db_dict)

    def retrieve_db_raw(self, db_id: str, use_cache: bool = True) -> dict[str, Any]:
        """Retreives the database and returns the raw response.

        Attributes:
            db_id: The id of the database to retrieve.

        Returns:
            The raw database.

        Raises:
            APIResponseError:
                Raised when the Notion API returns a status code that's not 2xx.
            HTTPError:
                Raised when there's some error when making the API call.
        """

        self._logger.info(f" Retrieving database {db_id}")
        endpoint = APIEndpoints.DB_RETRIEVE.value.format(db_id)

        if not use_cache:
            return self._make_request.__wrapped__(endpoint)
        return self._make_request(endpoint)

    def query_db(self, query: dict[str, Any]) -> list[Page]:

        query_results_dict = self.query_db_raw(query)
        return [Page.from_dict(page) for page in query_results_dict["results"]]

    def query_db_raw(self, query: dict[str, Any]) -> dict[str, Any]:

        raise NotImplementedError("querying databases isn't implemented yet")

    def create_db(self, db: dict[str, Any]) -> dict[str, Any]:

        raise NotImplementedError("creating databases isn't implemented yet")

    def update_db(self, db: dict[str, Any]) -> dict[str, Any]:

        raise NotImplementedError("updating databases isn't implemented yet")

    # ----- Page related endpoints -----

    def retrieve_page(self, page_id: str) -> Page:

        page_dict = self.retrieve_page_raw(page_id)
        return Page.from_dict(page_dict)

    def retrieve_page_raw(self, page_id: str) -> dict[str, Any]:

        raise NotImplementedError("retrieval of pages isn't implemented yet")

    def create_page(self, page: dict[str, Any]) -> dict[str, Any]:

        raise NotImplementedError()

    def update_page(self, page: dict[str, Any]) -> dict[str, Any]:

        raise NotImplementedError()

    # ---- Block related endpoints -----

    def retrieve_block(self, block_id: str) -> Block:
        raise NotImplementedError()

    def retrieve_block_raw(self, block_id: str) -> dict[str, Any]:

        endpoint = APIEndpoints.BLOCK_RETRIEVE.value.format(block_id)
        return self._make_request(endpoint)

    def update_block(self, block: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError()

    def retrieve_block_children_raw(self, block_id: str) -> dict[str, Any]:
        raise NotImplementedError()

    def append_block_child(self, block: str) -> dict[str, Any]:
        raise NotImplementedError()

    def delete_block(self, block_id: str) -> dict[str, Any]:
        raise NotImplementedError()

    # ----- Comment related endpoints -----

    def retrieve_comment(self, comment_id: str) -> Comment:
        raise NotImplementedError()

    def create_comment(self, comment: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError()

    # ----- User related endpoints -----

    def retrieve_user(self, user_id: str) -> User:
        raise NotImplementedError()

    def retrieve_user_raw(self, user_id: str) -> dict[str, Any]:

        endpoint = APIEndpoints.USER_RETRIEVE.value.format(user_id)
        return self._make_request(endpoint)

    def list_users(self) -> dict[str, Any]:
        raise NotImplementedError()

    def retrieve_me_raw(self) -> dict[str, Any]:

        endpoint = APIEndpoints.USER_TOKEN_BOT.value
        return self._make_request(endpoint)

    # ----- Search -----

    def search(self) -> dict[str, Any]:
        raise NotImplementedError()

    # ----- Miscellaneous -----
    def close(self):
        """Closes the client and cleans up all the resources."""

        self._client.close()

    def clear_cache(self):
        """Clears the cache."""

        self._make_request.cache_clear()

    def cache_info(self):
        """Returns the cache information."""

        return self._make_request.cache_info()

    # ----- Private Methods -----

    @lru_cache(maxsize=128)
    def _make_request(
        self,
        endpoint: str,
        method: Literal["get", "post", "put", "patch", "delete"] = "get",
        data: Optional[dict[Any, Any]] = None,
        query_params: Optional[dict[str, str]] = None,
    ):

        log_msg = (
            f" {method.upper()} request to {str(self._client.base_url) + endpoint}"
        )
        self._logger.debug(log_msg)
        self._logger.debug(f" Data: {data}")
        self._logger.debug(f" Query Params: {query_params}")

        if method == "get":
            resp = self._client.get(endpoint, params=query_params)
        elif method == "post":
            resp = self._client.post(endpoint, data=data, params=query_params)
        elif method == "put":
            resp = self._client.put(endpoint, data=data, params=query_params)
        elif method == "patch":
            resp = self._client.patch(endpoint, data=data, params=query_params)
        else:
            resp = self._client.delete(endpoint, params=query_params)

        return self._parse_response(resp)

    def _parse_response(self, resp: httpx.Response) -> dict[str, Any]:

        try:
            resp.raise_for_status()
        except httpx.HTTPStatusError as error:
            try:
                body = error.response.json()
                raise APIResponseError(error.response, body["code"], body["message"])
            except JSONDecodeError:
                raise HTTPError(error.response)

        response_dict = resp.json()
        self._logger.debug(f" Response: {response_dict}")
        return response_dict

    def _get_client(self) -> httpx.Client:

        base_headers: dict[str, str] = {
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": self._config.api_version,
        }
        transport = httpx.HTTPTransport(retries=self._config.retries)

        return httpx.Client(
            transport=transport,
            timeout=self._config.timeout,
            headers=base_headers,
            base_url=self._config.base_url,
        )

    def _get_logger(self) -> logging.Logger:

        if self._config.logger:
            return self._config.logger

        logger = make_logger()
        logger.setLevel(self._config.log_level)
        return logger

    # ----- Context Managers -----

    def __enter__(self):

        self._client.__enter__()
        return self

    def __exit__(
        self,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        traceback: TracebackType,
    ):

        self._client.__exit__(exc_type, exc_value, traceback)
