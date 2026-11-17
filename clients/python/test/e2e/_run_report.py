"""Session fixtures that report on the run: the cell of the matrix it tested, and the credits it
may spend on the deployment.

conftest.py registers this module from pytest_configure, since the test conventions keep autouse
fixtures out of conftest.py.
"""

import logging
import os
from collections.abc import Callable

import osparc
import pytest

_logger = logging.getLogger(__name__)


@pytest.fixture(scope="session", autouse=True)
def record_run_in_junit(request: pytest.FixtureRequest) -> None:
    """Writes deployment and client version into the junit report as testsuite properties.

    summarize_junit.py builds the client-by-deployment table from them.
    """
    if not getattr(request.config.option, "xmlpath", None):
        return
    record: Callable[[str, str], None] = request.getfixturevalue(
        "record_testsuite_property"
    )
    record("osparc_deployment", os.environ.get("OSPARC_API_HOST", "unset"))
    record("osparc_client_version", osparc.__version__)


@pytest.fixture(scope="session", autouse=True)
def log_wallet_budget(api_client: osparc.ApiClient) -> None:
    """Logs the default wallet's available credits before the first job.

    A billable deployment answers 402 to a job start it cannot pay for; a non-billable one answers
    404 to the wallet endpoints. Neither is a fault of the client, so neither fails here.
    """
    host = os.environ.get("OSPARC_API_HOST", "")
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
