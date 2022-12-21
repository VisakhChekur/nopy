import logging
import os
from dataclasses import dataclass
from json import JSONDecodeError
from types import TracebackType
from typing import Any
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

        self._configure_client()

    # ------ Database related endpoints ------

    def retrieve_db(self, db_id: str) -> Database:
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

        self._logger.info(f"Retrieving database {db_id}")
        endpoint = APIEndpoints.DB_RETRIEVE.value.format(db_id)
        db_dict = self._make_request(endpoint)

        db = Database.from_dict(db_dict)
        db._client = self  # type: ignore
        return db

    def query_db(self, db_id: str, query: dict[str, Any]) -> list[Page]:

        query_results_dict = self._query_db_raw(query, db_id)

        pages: list[Page] = []
        for res in query_results_dict["results"]:
            page = Page.from_dict(res)
            page._client = self  # type: ignore

        return pages

    def create_db(self, db: dict[str, Any]) -> dict[str, Any]:

        raise NotImplementedError("creating databases isn't implemented yet")

    def update_db(self, db: dict[str, Any]) -> dict[str, Any]:

        raise NotImplementedError("updating databases isn't implemented yet")

    # ----- Page related endpoints -----

    def retrieve_page(self, page_id: str) -> Page:

        self._logger.info(f"Retrieving page {page_id}")
        endpoint = APIEndpoints.PAGE_RETRIEVE.value.format(page_id)
        page = self._make_request(endpoint)
        return Page.from_dict(page)

    def create_page(self, page: dict[str, Any]) -> dict[str, Any]:

        raise NotImplementedError()

    def update_page(self, page: dict[str, Any]) -> dict[str, Any]:

        raise NotImplementedError()

    # ---- Block related endpoints -----

    def retrieve_block(self, block_id: str) -> Block:
        raise NotImplementedError()

    def update_block(self, block: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError()

    def retrieve_block_children(self, block_id: str) -> list[Block]:

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

    def list_users(self) -> list[User]:

        raise NotImplementedError()

    def retrieve_me(self) -> dict[str, Any]:

        endpoint = APIEndpoints.USER_TOKEN_BOT.value
        return self._make_request(endpoint)

    # ----- Search -----

    def search(self) -> dict[str, Any]:
        raise NotImplementedError()

    # ----- Miscellaneous -----
    def close(self):
        """Closes the client and cleans up all the resources."""

        self._client.close()

    # ----- Private Methods -----

    def _query_db_raw(self, query: dict[str, Any], db_id: str) -> dict[str, Any]:

        self._logger.info(f" Querying '{db_id}'")
        endpoint = APIEndpoints.DB_QUERY.value.format(db_id)
        return self._make_request(endpoint, "post", data=query)

    def _make_request(
        self,
        endpoint: str,
        method: str = "get",
        data: Optional[dict[Any, Any]] = None,
        query_params: Optional[dict[str, str]] = None,
    ):

        request = self._client.build_request(
            method, endpoint, json=data, params=query_params
        )

        log_msg = f" {request.method} request to {request.url}"
        self._logger.info(log_msg)
        self._logger.debug(f" Data: {data}")
        self._logger.debug(f" Query Params: {query_params}")

        resp = self._client.send(request)
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

    def _configure_client(self):

        # Configuring the logger
        if self._config.logger:
            self._logger = self._config.logger
        else:
            self._logger = make_logger(self._config.log_level)

        # Configuring the httpx client
        base_headers: dict[str, str] = {
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": self._config.api_version,
        }
        transport = httpx.HTTPTransport(retries=self._config.retries)
        self._client = httpx.Client(
            transport=transport,
            timeout=self._config.timeout,
            headers=base_headers,
            base_url=self._config.base_url,
        )

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
