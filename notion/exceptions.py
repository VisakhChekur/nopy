class NotionError(Exception):
    """Base class for all Notion exceptions."""

    def __init__(self, message: str):
        super().__init__(message)


class AuthenticationError(NotionError):
    """Authentication issue when connecting to Notion API."""

    pass
