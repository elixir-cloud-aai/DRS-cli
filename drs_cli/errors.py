import logging
from types import TracebackType

logger = logging.getLogger(__name__)


def exception_handler(
    _type: type,
    value: BaseException,
    traceback: TracebackType
) -> None:
    """Error handler for all exceptions."""
    if str(value):
        msg = f"{_type.__name__}: {value}"
    else:
        msg = f"{_type.__name__}"
    logger.error(msg)


class InvalidObjectData(Exception):
    """Exception raised when object data cannot be validated against the API
    schema.
    """


class InvalidResponseError(Exception):
    """Exception raised when an invalid API response is encountered."""


class InvalidURI(Exception):
    """Exception raised for invalid URIs."""
