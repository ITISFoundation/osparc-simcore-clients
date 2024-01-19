from functools import wraps

from httpx import HTTPStatusError
from osparc_client import ApiException


class VisibleDeprecationWarning(UserWarning):
    """Visible deprecation warning.

    Acknowledgement: Having this wrapper is borrowed from numpy
    """


def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HTTPStatusError as e:
            raise ApiException(f"{e}") from e

    return wrapper
