# pylint: disable=protected-access
# pylint: disable=redefined-outer-name
# pylint: disable=too-many-arguments
# pylint: disable=unused-argument
# pylint: disable=unused-variable

import contextlib
import datetime
import logging
import os
from collections.abc import Iterable
from pathlib import Path
from typing import Final, NamedTuple
from uuid import UUID

import httpx2
import osparc
import pytest
from httpx2 import AsyncClient, BasicAuth
from memory_profiler import memory_usage
from numpy import random
from packaging.version import InvalidVersion, Version
from pydantic import ByteSize

with contextlib.suppress(ImportError):
    from osparc._settings import ConfigurationEnvVars

# DEBUG on osparc logs every request/response header, Authorization included, so it is
# opt-in through OSPARC_E2E_HTTP_DEBUG instead of on by default.
if os.environ.get("OSPARC_E2E_HTTP_DEBUG"):
    logging.getLogger("osparc").setLevel(logging.DEBUG)

_KB: ByteSize = ByteSize(1024)  # in bytes
_MB: ByteSize = ByteSize(_KB * 1024)  # in bytes
_GB: ByteSize = ByteSize(_MB * 1024)  # in bytes

_logger = logging.getLogger(__name__)

# Dictionary to store start times of tests
_test_start_times = {}

# A CI run labels itself with the client version it installed. That label is optional, and
# when present it must match what is importable, else the reported result belongs to another
# client than the one that ran.
_CLIENT_VERSION_LABEL_ENV_VAR: Final[str] = "OSPARC_CLIENT_VERSION"
_LATEST_CLIENT_VERSION_LABELS: Final[set[str]] = {"latest_release", "latest_master"}
_META_TIMEOUT_SECONDS: Final[float] = 10.0


def _utc_now():
    return datetime.datetime.now(tz=datetime.UTC)


def _construct_graylog_url(api_host, start_time, end_time):
    """
    Construct a Graylog URL for the given time interval.
    """
    base_url = api_host.replace("api.", "monitoring.", 1).rstrip("/")
    url = f"{base_url}/graylog/search"
    start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    end_time_str = end_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    query = f"from={start_time_str}&to={end_time_str}"
    return f"{url}?{query}"


def _check_client_version_label() -> None:
    label = os.environ.get(_CLIENT_VERSION_LABEL_ENV_VAR)
    if not label or label in _LATEST_CLIENT_VERSION_LABELS:
        return
    try:
        expected = Version(label)
    except InvalidVersion as exc:
        raise pytest.UsageError(
            f"{_CLIENT_VERSION_LABEL_ENV_VAR}={label} is not a valid version"
        ) from exc
    if expected != Version(osparc.__version__):
        raise pytest.UsageError(
            f"{_CLIENT_VERSION_LABEL_ENV_VAR}={label} does not match the installed "
            f"osparc {osparc.__version__}"
        )


def _server_api_version(host: str) -> str:
    if not host:
        return "unknown, no host set"
    try:
        response = httpx2.get(
            f"{host.rstrip('/')}/v0/meta", timeout=_META_TIMEOUT_SECONDS
        )
        response.raise_for_status()
        return str(response.json().get("version", "unknown"))
    except (httpx2.HTTPError, ValueError) as exc:
        return f"unreachable ({exc.__class__.__name__})"


def pytest_report_header(config: pytest.Config) -> list[str]:
    """Log what is being tested against what, before the first test runs."""
    host = os.environ.get("OSPARC_API_HOST", "")
    return [
        f"osparc client: {osparc.__version__}",
        f"deployment: {host or 'OSPARC_API_HOST not set'}"
        f" (api-server {_server_api_version(host)})",
    ]


def pytest_runtest_setup(item):
    """
    Hook to capture the start time of each test.
    """
    _test_start_times[item.name] = _utc_now()


def pytest_runtest_makereport(item, call):
    """
    Hook to add extra information when a test fails.
    """
    # only report on a failed test call
    if call.when == "call" and call.excinfo is not None:
        test_name = item.name
        test_location = item.location
        api_host = os.environ.get("OSPARC_API_HOST", "")

        diagnostics = {
            "test_name": test_name,
            "test_location": test_location,
            "api_host": api_host,
        }

        # Get the start and end times of the test
        start_time = _test_start_times.get(test_name)
        end_time = _utc_now()

        if start_time:
            diagnostics["graylog_url"] = _construct_graylog_url(
                api_host, start_time, end_time
            )

        # Print the diagnostics
        print(f"\nDiagnostics for {test_name}:")
        for key, value in diagnostics.items():
            print("  ", key, ":", value)


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    _check_client_version_label()
    config.pluginmanager.register(pytest_runtest_setup, "osparc_test_times_plugin")
    config.pluginmanager.register(pytest_runtest_makereport, "osparc_makereport_plugin")


@pytest.fixture(scope="session")
def api_client() -> Iterable[osparc.ApiClient]:
    if Version(osparc.__version__) >= Version("0.8.0"):
        with osparc.ApiClient() as api_client:
            api_client.configuration.debug = True
            yield api_client
    else:
        host = os.environ.get("OSPARC_API_HOST")
        username = os.environ.get("OSPARC_API_KEY")
        password = os.environ.get("OSPARC_API_SECRET")
        assert host and username and password
        configuration = osparc.Configuration(
            host=host, username=username, password=password
        )
        configuration.debug = True
        with osparc.ApiClient(configuration=configuration) as api_client:
            yield api_client


@pytest.fixture(scope="session")
def files_api(api_client: osparc.ApiClient) -> osparc.FilesApi:
    return osparc.FilesApi(api_client=api_client)


@pytest.fixture
def async_client() -> Iterable[AsyncClient]:
    if Version(osparc.__version__) >= Version("8.0.0"):
        configuration = ConfigurationEnvVars()
        host = configuration.OSPARC_API_HOST.rstrip("/")
        username = configuration.OSPARC_API_KEY
        password = configuration.OSPARC_API_SECRET
    else:
        host = os.environ.get("OSPARC_API_HOST")
        username = os.environ.get("OSPARC_API_KEY")
        password = os.environ.get("OSPARC_API_SECRET")
        assert host and username and password
    yield AsyncClient(
        base_url=host,
        auth=BasicAuth(
            username=username,
            password=password,
        ),
    )  # type: ignore


class ServerFile(NamedTuple):
    server_file: osparc.File
    local_file: Path
    upload_ram_usage: int


@pytest.fixture(scope="session")
def large_server_file(
    files_api: osparc.FilesApi, tmp_path_factory
) -> Iterable[ServerFile]:
    _file_size: Final[ByteSize] = ByteSize(1 * _GB)
    tmp_file = (
        tmp_path_factory.mktemp(basename=large_server_file.__name__)
        / "large_test_file.txt"
    )
    ss: random.SeedSequence = random.SeedSequence()
    logging.info("Entropy used to generate random file: %s", f"{ss.entropy}")
    rng: random.Generator = random.default_rng(ss)
    tmp_file.write_bytes(rng.bytes(1000))
    with open(tmp_file, "wb") as f:
        f.truncate(_file_size)
    assert tmp_file.stat().st_size == _file_size, (
        f"Could not create file of size: {_file_size}"
    )
    ram_statistics, uploaded_file = memory_usage(
        (files_api.upload_file, (tmp_file,)), retval=True
    )

    yield ServerFile(
        local_file=tmp_file,
        server_file=uploaded_file,
        upload_ram_usage=max(ram_statistics) - min(ram_statistics),
    )

    try:
        files_api.delete_file(uploaded_file.id)
    except osparc.ApiException:
        _logger.warning(
            f"Could not delete file on server in {file_with_number.__name__}",
            exc_info=True,
        )


@pytest.fixture
def sleeper(api_client: osparc.ApiClient) -> osparc.Solver:
    solvers_api = osparc.SolversApi(api_client=api_client)
    sleeper: osparc.Solver = solvers_api.get_solver_release(
        "simcore/services/comp/itis/sleeper", "2.0.2"
    )  # type: ignore
    return sleeper


@pytest.fixture
def sleeper_study_id(api_client: osparc.ApiClient) -> UUID:
    """Simple sleeper study template which takes
    as input a single file containing a single integer"""
    _test_study_title = "sleeper_test_study"
    study_api = osparc.StudiesApi(api_client=api_client)

    def _ensure_uid(study):
        return study.uid if isinstance(study.uid, UUID) else UUID(study.uid)

    study_ids = [
        _ensure_uid(study)
        for study in study_api.iter_studies()
        if study.title == _test_study_title
    ]
    assert len(study_ids) == 1, (
        f"Found multiple {_test_study_title} studies"
        if len(study_ids) > 1
        else f"Could not find {_test_study_title} study"
    )
    return study_ids[0]


@pytest.fixture
def file_with_number(
    tmp_path: Path, api_client: osparc.ApiClient
) -> Iterable[osparc.File]:
    files_api = osparc.FilesApi(api_client=api_client)
    file = tmp_path / "file_with_number.txt"
    file.write_text("1")
    server_file = files_api.upload_file(file)
    yield server_file

    try:
        files_api.delete_file(server_file.id)
    except osparc.ApiException:
        _logger.warning(
            f"Could not delete file on server in {file_with_number.__name__}",
            exc_info=True,
        )
