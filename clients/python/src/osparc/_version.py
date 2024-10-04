import warnings
from platform import python_version
from packaging.version import Version
from ._exceptions import VisibleDeprecationWarning

from osparc_client import __version__ as __version__


_PYTHON_VERSION_RETIRED = Version("3.8.0")
_PYTHON_VERSION_DEPRECATED = Version("3.8.0")
assert _PYTHON_VERSION_RETIRED <= _PYTHON_VERSION_DEPRECATED  # nosec

if Version(python_version()) < _PYTHON_VERSION_RETIRED:
    error_msg: str = (
        f"Python version {python_version()} is retired for this version of osparc. "
        f"Please use Python version {_PYTHON_VERSION_DEPRECATED}."
    )
    raise RuntimeError(error_msg)

if Version(python_version()) < _PYTHON_VERSION_DEPRECATED:
    warning_msg: str = (
        f"Python {python_version()} is deprecated. "
        "Please upgrade to "
        f"Python version >= {_PYTHON_VERSION_DEPRECATED}."
    )
    warnings.warn(warning_msg, VisibleDeprecationWarning)
