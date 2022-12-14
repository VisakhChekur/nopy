class NotionError(Exception):
    """Base class for all Notion exceptions."""

    pass


class NotionAPIError(NotionError):
    """Any error that took place during the call to the Notion API."""


class AuthenticationError(NotionAPIError):
    """Authentication issue when connecting to Notion API."""

    pass


class NotFoundError(NotionAPIError):
    """Requested resource wasn't found."""

    pass


class FormatError(NotionAPIError):
    """Invalid format."""

    pass


class UnsupportedError(NotionError):
    """Unsupported by Notion or by this library."""

    pass


class SerializationError(NotionError):
    """Error that took place during serialization."""

    pass


class MappingError(NotionError):
    """Error that took place while mapping the response from the Notion
    API into the corresponding Notion object."""

    pass
