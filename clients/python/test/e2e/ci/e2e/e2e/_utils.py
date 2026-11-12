from enum import IntEnum
from functools import wraps

import pytest
import typer
from pydantic import ValidationError


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
    SKIPPING_TESTS = 101
    INVALID_JSON_DATA = 102


assert {e.value for e in E2eExitCodes}.intersection(
    {e.value for e in pytest.ExitCode}
) == set()


def handle_validation_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValidationError, ValueError) as e:
            typer.echo(f"{e}", err=True)
            raise typer.Exit(code=E2eExitCodes.INVALID_JSON_DATA) from e

    return wrapper
