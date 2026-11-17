"""Session fixtures that report on the run: the cell of the matrix it tested, and the credits it
may spend on the deployment.

conftest.py registers this module from pytest_configure, since the test conventions keep autouse
fixtures out of conftest.py.
"""

import logging
from collections.abc import Callable
from typing import Final

import osparc
import pytest
from packaging.version import Version

_logger: Final[logging.Logger] = logging.getLogger(__name__)

_SLEEPER_KEY: Final[str] = "simcore/services/comp/itis/sleeper"

# Set by the session fixture below, read by conftest.pytest_terminal_summary. A run that never
# got a client keeps it empty and reports nothing.
_sleeper_releases: Final[list[str]] = []


def sleeper_releases() -> str:
    """What the deployment offers for sleeper, as one line for the run summary."""
    return ", ".join(_sleeper_releases)


def _deployment(api_client: osparc.ApiClient) -> str:
    """Host the client talks to, as its configuration resolved it."""
    return api_client.configuration.host.rstrip("/") or "unset"


def _list_sleeper_releases(api_client: osparc.ApiClient) -> list[str]:
    """The versions the deployment offers for sleeper, oldest first.

    Which releases a deployment carries decides what the suite can run on it, so the summary
    names them.
    """
    solvers_api = getattr(osparc, "SolversApi", None)
    if solvers_api is None:
        return []
    try:
        releases = solvers_api(api_client=api_client).list_solver_releases(_SLEEPER_KEY)
    except Exception as exc:  # noqa: BLE001
        _logger.info(
            "deployment %s: sleeper releases could not be listed (%s)",
            _deployment(api_client),
            exc.__class__.__name__,
        )
        return []
    return sorted((release.version for release in releases), key=Version)


@pytest.fixture(scope="session", autouse=True)
def _record_run_in_junit(
    request: pytest.FixtureRequest, api_client: osparc.ApiClient
) -> None:
    """Writes the deployment, the client version and the deployment's sleeper releases as junit
    testsuite properties.

    summarize_junit.py builds the client-by-deployment table from the first two. The releases go
    to conftest.pytest_terminal_summary as well, which runs whether or not a report is written.
    """
    _sleeper_releases.extend(_list_sleeper_releases(api_client))
    if not getattr(request.config.option, "xmlpath", None):
        return
    record: Callable[[str, str], None] = request.getfixturevalue(
        "record_testsuite_property"
    )
    record("osparc_deployment", _deployment(api_client))
    record("osparc_client_version", osparc.__version__)
    record("osparc_sleeper_releases", sleeper_releases() or "none")


@pytest.fixture(scope="session", autouse=True)
def _log_wallet_budget(api_client: osparc.ApiClient) -> None:
    """Logs the default wallet's available credits before the first job.

    A billable deployment answers 402 to a job start it cannot pay for; a non-billable one answers
    404 to the wallet endpoints. Neither is a fault of the client, so neither fails here.
    """
    host = _deployment(api_client)
    wallets_api = getattr(osparc, "WalletsApi", None)
    if wallets_api is None:
        _logger.info(
            "deployment %s: osparc %s has no wallets API, billing cannot be reported",
            host,
            osparc.__version__,
        )
        return
    try:
        wallet = wallets_api(api_client=api_client).get_default_wallet()
    except Exception as exc:  # noqa: BLE001
        _logger.info(
            "deployment %s: no default wallet (%s), so billing is off or unsupported here",
            host,
            exc.__class__.__name__,
        )
        return
    _logger.info(
        "deployment %s: default wallet %r has %s credits available",
        host,
        wallet.name,
        getattr(wallet, "available_credits", "unknown"),
    )
