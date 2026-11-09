import calendar
import os
import sys
import warnings
from datetime import date
from typing import Dict, Final

from ._exceptions import VisibleDeprecationWarning

# One ISO end-of-life date per interpreter cycle, copied from
# https://endoflife.date/api/python.json. scripts/check-python-eol-dates.bash
# re-fetches that API and fails CI when this table no longer matches it.
_PYTHON_EOL_DATES: Final[Dict[str, str]] = {
    "3.11": "2027-10-31",
    "3.12": "2028-10-31",
    "3.13": "2029-10-31",
    "3.14": "2030-10-31",
    "3.15": "2031-10-31",
}

# An interpreter inside this window gets a warning at import.
_WARNING_WINDOW_MONTHS: Final[int] = 3

# Read from the environment directly, not through the pydantic-settings models in
# `_settings.py`: this runs while `import osparc` is still executing.
_DISABLE_WARNING_ENV_VAR: Final[str] = "OSPARC_DISABLE_PYTHON_EOL_WARNING"
_DISABLED_VALUES: Final[frozenset[str]] = frozenset({"1", "true", "yes"})


def _add_months(when: date, months: int) -> date:
    """Adds calendar months, rolling the year and clamping the day to the last
    day of the target month.
    """
    total = (when.year * 12 + when.month - 1) + months
    year, month_index = divmod(total, 12)
    month = month_index + 1
    last_day = calendar.monthrange(year, month)[1]
    return date(year, month, min(when.day, last_day))


def _whole_months_until(from_day: date, to_day: date) -> int:
    """Whole calendar months left in `from_day` until `to_day`. A part-month
    does not count, so fewer than a full month left gives 0.
    """
    raw = (to_day.year - from_day.year) * 12 + (to_day.month - from_day.month)
    return raw - 1 if to_day.day < from_day.day else raw


def _major_minor(version: str) -> str:
    """The "major.minor" cycle of a version string such as "3.11.4"."""
    major, minor, *_ = version.split(".")
    return f"{int(major)}.{int(minor)}"


def _warning_is_disabled() -> bool:
    return os.environ.get(_DISABLE_WARNING_ENV_VAR, "").lower() in _DISABLED_VALUES


def check_python_eol(*, version: str | None = None, today: date | None = None) -> None:
    """Warns when the running interpreter is at or close to its end-of-life date.

    Never raises: a failing interpreter check must not block the client.

    `version` and `today` let tests fix the cycle and the date rather than patch
    the clock. `version` takes a full version such as "3.11.4" and resolves it to
    its cycle. A cycle missing from the table, a future interpreter, is ignored.
    """
    if _warning_is_disabled():
        return

    now = date.today() if today is None else today
    try:
        cycle = (
            f"{sys.version_info.major}.{sys.version_info.minor}"
            if version is None
            else _major_minor(version)
        )
        end_of_life = date.fromisoformat(_PYTHON_EOL_DATES[cycle])
    except (KeyError, ValueError):
        return

    if now >= end_of_life:
        message: str = (
            f"Python {cycle} reached end of life on {end_of_life}. It no longer "
            "receives security fixes; please upgrade to a supported Python version."
        )
    elif _add_months(now, _WARNING_WINDOW_MONTHS) >= end_of_life:
        months_left = _whole_months_until(now, end_of_life)
        if months_left >= 1:
            unit = "month" if months_left == 1 else "months"
            remaining = f"in {months_left} {unit}"
        else:
            remaining = "in less than a month"
        message = (
            f"Python {cycle} reaches end of life on {end_of_life} {remaining}. "
            "Please plan an upgrade to a supported Python version."
        )
    else:
        return

    warnings.warn(message, VisibleDeprecationWarning, stacklevel=2)
