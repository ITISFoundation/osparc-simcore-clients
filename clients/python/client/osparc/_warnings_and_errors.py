from functools import wraps

from httpx import HTTPStatusError


class VisibleDeprecationWarning(UserWarning):
    """Visible deprecation warning.

    Acknowledgement: Having this wrapper is borrowed from numpy
    """


class RequestError(Exception):
    """For exceptions encountered when performing HTTP requests."""


def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HTTPStatusError as e:
            raise RequestError(f"{e}") from e

    return wrapper
