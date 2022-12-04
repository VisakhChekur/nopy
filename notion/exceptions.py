class NotionError(Exception):
    """Base class for all Notion exceptions."""

    pass

class AuthenticationError(NotionError):
    """Authentication issue when connecting to Notion API."""

    pass


class NotFoundError(NotionError):
    """Requested resource wasn't found."""

    pass

class ValidationError(NotionError):
    """Invalid format."""

    pass

class UnsupportedError(NotionError):
    """Unsupported by Notion or by this library."""
    pass