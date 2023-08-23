class VisibleDeprecationWarning(UserWarning):
    """Visible deprecation warning.

    Acknowledgement: Having this wrapper is borrowed from numpy
    """


class RequestError(Exception):
    """For exceptions encountered when performing HTTP requests."""
