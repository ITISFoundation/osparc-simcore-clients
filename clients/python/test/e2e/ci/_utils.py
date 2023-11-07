from enum import IntEnum
from pathlib import Path

import pytest

# Paths -------------------------------------------------------

_E2E_DIR: Path = Path(__file__).parent.parent.resolve()
_PYTHON_DIR: Path = _E2E_DIR.parent.parent
_CI_DIR: Path = (_E2E_DIR / "ci").resolve()
_PYTEST_INI: Path = (_E2E_DIR / "pytest.ini").resolve()
_ARTIFACTS_DIR: Path = (_E2E_DIR.parent.parent / "artifacts" / "e2e").resolve()
_COMPATIBILITY_CSV: Path = (
    _E2E_DIR / "data" / "server_client_compatibility.csv"
).resolve()

assert _COMPATIBILITY_CSV.is_file()


def print_line():
    """Print a line in log"""
    print(150 * "=")


# classed for handling errors ----------------------------------
class E2eScriptFailure(UserWarning):
    """Simply used to indicate a CI script failure"""

    pass


class E2eExitCodes(IntEnum):
    """Exitcodes
    Note these should not clash with pytest exitcodes:
    https://docs.pytest.org/en/7.1.x/reference/exit-codes.html
    """

    CI_SCRIPT_FAILURE = 100
    INCOMPATIBLE_CLIENT_SERVER = 101
    INVALID_JSON_DATA = 102


assert (
    set(e.value for e in E2eExitCodes).intersection(
        set(e.value for e in pytest.ExitCode)
    )
    == set()
)
