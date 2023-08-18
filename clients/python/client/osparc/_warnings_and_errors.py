import aiohttp


class VisibleDeprecationWarning(UserWarning):
    """Visible deprecation warning.

    Acknowledgement: Having this wrapper is borrowed from numpy
    """


class RequestError(Exception):
    """For exceptions encountered when performing HTTP requests."""


def aiohttp_error_handler_async(method):
    """Handle Aiohttp errors"""

    async def wrapper(*args, **kwargs):
        try:
            return await method(*args, **kwargs)
        except aiohttp.ClientResponseError as err:
            msg = f"HTTP status: {err.code}. {err.message}"
            raise RequestError(msg) from err

    return wrapper
