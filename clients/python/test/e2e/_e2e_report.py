"""Reports on the run itself: what it ran against, and what it may spend.

Registered by conftest.py's pytest_configure rather than left in that file, which holds no autouse
fixtures on purpose. Both fixtures here apply to every test in the session.
"""

import logging
import os

import osparc
import pytest

_logger = logging.getLogger(__name__)


@pytest.fixture(scope="session", autouse=True)
def record_run_in_junit(request: pytest.FixtureRequest) -> None:
    """Writes deployment and client version into the junit report.

    Each cell of the matrix is a separate job with its own report, and the file name is not enough
    to say which one it was. summarize_junit.py reads these two properties back.
    """
    if not getattr(request.config.option, "xmlpath", None):
        return
    record = request.getfixturevalue("record_testsuite_property")
    record("osparc_deployment", os.environ.get("OSPARC_API_HOST", "unset"))
    record("osparc_client_version", osparc.__version__)


@pytest.fixture(scope="session", autouse=True)
def log_wallet_budget(api_client: osparc.ApiClient) -> None:
    """Logs the default wallet's credits before the first job.

    A billable deployment refuses a job start it cannot pay for with 402, and on a non-billable one
    the wallet endpoints answer 404. Neither is a fault here, so both are only reported.
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
