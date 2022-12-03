import os

from notion.exceptions import AuthenticationError


class NotionClient:
    """A client to connect with Notion using the official Notion API."""

    def __init__(self, token: str = ""):
        """Constructor for client.

        Args:
            token:
                The Notion token from the Notion integration. If it's not
                provided, then the value must be present in the environment
                variables with the name `NOTION_TOKEN`.

        Raises:
            AuthenticationError: Token not found.
        """

        try:
            self._token = token or os.environ.get("NOTION_TOKEN")
        except KeyError:
            raise AuthenticationError(
                "Token not provided and not found from environment variables with name `NOTION_TOKEN`"
            )
