from platform import python_version
from typing import Final

from osparc_client import __version__ as __version__
from packaging.version import Version

from ._python_eol import check_python_eol

# The floor `python_requires` in setup.py declares. pip will not install below
# it, so importing here means an environment built outside the package metadata.
_PYTHON_VERSION_FLOOR: Final[Version] = Version("3.11")

if Version(python_version()) < _PYTHON_VERSION_FLOOR:
    error_msg: str = (
        f"Python version {python_version()} is not supported by this version of osparc. "
        f"Please use Python version >= {_PYTHON_VERSION_FLOOR}."
    )
    raise RuntimeError(error_msg)

check_python_eol()
