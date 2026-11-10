# The end-of-life check takes the cycle and the date as arguments, so these tests fix
# both instead of patching the clock or the interpreter.
import importlib
import platform
import re
import sys
import warnings
from datetime import date, timedelta
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Final, List

import osparc._python_eol as _python_eol
import osparc._version as _version
import pytest
from osparc._exceptions import VisibleDeprecationWarning
from osparc._python_eol import (
    _DISABLE_WARNING_ENV_VAR,
    _PYTHON_EOL_DATES,
    _WARNING_WINDOW_MONTHS,
    _add_months,
    check_python_eol,
)

_REPO_ROOT: Final[Path] = Path(__file__).parents[4]
_MATRIX_FILE: Final[Path] = (
    _REPO_ROOT / ".github" / "workflows" / "build-python-client.yml"
)

# 3.11's end-of-life date, used by the dates in the cases below
_EOL: Final[date] = date(2027, 10, 31)


class _DateFrozenAtEndOfLife(date):
    """`date` standing still inside the warning window of Python 3.11."""

    @classmethod
    def today(cls) -> date:
        return _EOL


def _emit(**kwargs: Any) -> List[warnings.WarningMessage]:
    """Runs the check with warnings captured rather than printed."""
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        check_python_eol(**kwargs)
    return list(caught)


def test_add_months_clamps_to_the_last_day_of_the_month():
    assert _add_months(date(2027, 1, 31), 1) == date(2027, 2, 28)
    assert _add_months(date(2028, 1, 31), 1) == date(2028, 2, 29)
    assert _add_months(date(2027, 11, 15), 3) == date(2028, 2, 15)


@pytest.mark.parametrize(
    "today",
    [date(2027, 1, 1), _EOL - timedelta(days=93)],
    ids=["years-left", "one-day-before-the-window"],
)
def test_an_interpreter_with_time_left_is_silent(today: date):
    assert not _emit(version="3.11.4", today=today)


def test_the_check_does_not_raise_when_warnings_are_errors():
    # `PYTHONWARNINGS=error` makes `warnings.warn` raise. The check runs during
    # `import osparc`, so an interpreter at end of life must stay importable.
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        check_python_eol(version="3.11", today=_EOL)


def test_no_version_falls_back_to_the_running_interpreter(
    monkeypatch: pytest.MonkeyPatch,
):
    # this is the call `osparc/_version.py` makes at import
    monkeypatch.setattr(sys, "version_info", SimpleNamespace(major=3, minor=11))
    caught = _emit(today=_EOL)
    assert len(caught) == 1
    assert "Python 3.11" in str(caught[0].message)

    monkeypatch.setattr(sys, "version_info", SimpleNamespace(major=3, minor=12))
    assert not _emit(today=_EOL)


def test_the_window_opens_three_calendar_months_before_end_of_life():
    caught = _emit(version="3.11", today=_add_months(_EOL, -_WARNING_WINDOW_MONTHS))
    assert len(caught) == 1
    assert "in 3 months" in str(caught[0].message)


def test_a_patch_release_is_treated_as_its_cycle():
    assert len(_emit(version="3.11.18", today=date(2027, 9, 15))) == 1


@pytest.mark.parametrize(
    "today,expected",
    [
        (_EOL, "reached end of life"),
        (_EOL + timedelta(days=1), "reached end of life"),
        (date(2027, 8, 31), "in 2 months"),
        (date(2027, 9, 15), "in 1 month"),
        (date(2027, 10, 30), "in less than a month"),
    ],
    ids=[
        "at-end-of-life",
        "past-end-of-life",
        "two-months",
        "one-month",
        "partial-month",
    ],
)
def test_the_warning_names_the_date_and_the_time_left(today: date, expected: str):
    caught = _emit(version="3.11", today=today)
    assert len(caught) == 1
    message = caught[0].message
    assert isinstance(message, VisibleDeprecationWarning)
    assert expected in str(message)
    assert str(_EOL) in str(message)
    announced = re.search(r"in (\d+) month", str(message))
    if announced is not None:
        assert _add_months(today, int(announced.group(1))) <= _EOL


def test_the_countdown_rounds_down_to_whole_months():
    # one day into the warning window, 2 months and 30 days are left
    today = _add_months(_EOL, -_WARNING_WINDOW_MONTHS) + timedelta(days=1)
    caught = _emit(version="3.11", today=today)
    assert len(caught) == 1
    assert "in 2 months" in str(caught[0].message)


def test_the_end_of_life_message_mentions_security_fixes():
    caught = _emit(version="3.11", today=_EOL)
    assert "security fixes" in str(caught[0].message)


@pytest.mark.parametrize("value", ["1", "true", "TRUE", "yes"])
def test_the_environment_variable_suppresses_the_warning(
    monkeypatch: pytest.MonkeyPatch, value: str
):
    monkeypatch.setenv(_DISABLE_WARNING_ENV_VAR, value)
    assert not _emit(version="3.11", today=_EOL)


def test_the_environment_variable_does_not_suppress_on_any_other_value(
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.setenv(_DISABLE_WARNING_ENV_VAR, "0")
    assert _emit(version="3.11", today=_EOL)


def test_a_cycle_without_a_record_is_ignored():
    assert not _emit(version="3.99", today=date(2027, 10, 1))


def test_a_malformed_table_entry_never_raises(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setitem(_PYTHON_EOL_DATES, "3.11", "not a date")
    assert not _emit(version="3.11", today=date(2027, 10, 1))


def test_the_table_covers_every_interpreter_in_the_test_matrix():
    # the CI matrix decides which interpreters are supported, not this module
    matrix = re.search(
        r"python-version:\s*\[([^\]]*)\]", _MATRIX_FILE.read_text()
    ).group(1)
    for cycle in re.findall(r"\d+\.\d+", matrix):
        assert cycle in _PYTHON_EOL_DATES, f"no end-of-life date for Python {cycle}"


def test_importing_the_package_warns_once_on_an_eol_interpreter(
    monkeypatch: pytest.MonkeyPatch,
):
    # `_version.py` calls the check with no arguments, so the clock is pinned too
    monkeypatch.setattr(_python_eol, "date", _DateFrozenAtEndOfLife)
    monkeypatch.setattr(_version, "python_version", lambda: "3.11.10")
    monkeypatch.setattr(sys, "version_info", SimpleNamespace(major=3, minor=11))
    try:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            importlib.reload(_version)
    finally:
        monkeypatch.undo()
        importlib.reload(_version)
    assert len(caught) == 1
    assert isinstance(caught[0].message, VisibleDeprecationWarning)
    assert "Python 3.11" in str(caught[0].message)


def test_importing_the_package_is_silent_when_the_warning_is_disabled(
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.setattr(_python_eol, "date", _DateFrozenAtEndOfLife)
    monkeypatch.setattr(_version, "python_version", lambda: "3.11.10")
    monkeypatch.setenv(_DISABLE_WARNING_ENV_VAR, "true")
    monkeypatch.setattr(sys, "version_info", SimpleNamespace(major=3, minor=11))
    try:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            importlib.reload(_version)
    finally:
        monkeypatch.undo()
        importlib.reload(_version)
    assert not caught


def test_import_below_the_supported_floor_raises(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(platform, "python_version", lambda: "3.10.13")
    try:
        with pytest.raises(RuntimeError, match="not supported"):
            importlib.reload(_version)
    finally:
        # the package must stay importable for the rest of the session
        monkeypatch.undo()
        importlib.reload(_version)
