import httpx


class NopyError(Exception):
    """Base exception from which all Nopy errors inherit.

    This exception can be caught to catch all possible errors
    that may take place via the package.
    """

    pass


class TokenNotFoundError(NopyError):
    """Error raised when no Notion token was found."""

    pass


class HTTPError(NopyError):
    """Encompasses all errors that took place during the
    request to the Notion API.

    Attributes:
        status_code: The status code of the response.
        headers: The headers returned by the response.
        body: The body of the response as a string.
    """

    def __init__(self, response: httpx.Response, message: str = ""):

        if not message:
            message = f"Request to the Notion API failed with status code: {response.status_code}"

        super().__init__(message)
        self.status_code = response.status_code
        self.message = response.text
        self.body = response.headers


class APIResponseError(HTTPError):
    """Encompasses any error that is returned by the Notion API.

    Attributes:
        code: The error code returned by Notion.
        message: The error message returned by Notion.
    """

    def __init__(self, response: httpx.Response, code: str, message: str):

        error_message = f"{code.upper()} - {message}"
        super().__init__(response, error_message)

        self.code = code
        self.message = message


class UnuspportedError(NopyError):
    """An error raised when the user tries to do something that's not
    supported by the library or via the Notion API."""

    def __init__(self, message: str):

        super().__init__(message)


class UnsupportedByLibraryError(UnuspportedError):
    """An error raised when the user tries to do something that's not
    supported by the library currently."""

    def __init__(self, message: str):

        message += " is currently unsupported by the library"
        super().__init__(message)


class UnsupportedByNotion(UnuspportedError):
    """An error raised when the user tries to do something that's not
    supported by the Notion API currently."""

    def __init__(self, message: str):
        message += " is currently unsupported by the Notion API"
        super().__init__(message)
