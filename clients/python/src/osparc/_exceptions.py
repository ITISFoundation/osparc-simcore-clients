# pylint: disable=unused-import

from functools import wraps

from httpx import HTTPStatusError


from osparc_client.exceptions import ApiException as ApiException


class VisibleDeprecationWarning(UserWarning):
    """Visible deprecation warning.

    Acknowledgement: Having this wrapper is borrowed from numpy
    """


class RequestError(ApiException):
    pass


def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HTTPStatusError as e:
            raise RequestError(f"{e}") from e

    return wrapper
