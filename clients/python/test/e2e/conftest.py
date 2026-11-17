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
from typing import Any, Final, NamedTuple
from uuid import UUID, uuid4

import _e2e_report
import httpx2
import osparc
import pytest
from _utils import (
    UPLOADED_FILE,
    RecordedResource,
    record_resource,
)
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


def _record_uploaded_file(file_id: str | UUID) -> None:
    """Adds an upload to the resource log, so cleanup_resources.py can find it if the run is
    killed before the fixture's own teardown deletes it. Without the variable there is nowhere
    to record and nothing to do."""
    record_resource(
        RecordedResource(kind=UPLOADED_FILE, key="", version="", resource_id=file_id)
    )


# Dictionary to store start times of tests
_test_start_times = {}

# A CI run labels itself with the client version it installed. That label is optional, and
# when present it must match what is importable, else the reported result belongs to another
# client than the one that ran.
_CLIENT_VERSION_LABEL_ENV_VAR: Final[str] = "OSPARC_CLIENT_VERSION"
_LATEST_CLIENT_VERSION_LABELS: Final[set[str]] = {"latest_release", "latest_master"}
_META_TIMEOUT_SECONDS: Final[float] = 10.0

_SLEEPER_KEY: Final[str] = "simcore/services/comp/itis/sleeper"

# Fallback for an input port that declares no default, keyed by the jsonschema type. The suite
# only needs the job to run, so any value the port accepts is enough.
_INPUT_VALUE_BY_TYPE: Final[dict[str, Any]] = {
    "number": 1.0,
    "integer": 1,
    "boolean": False,
    "string": "false",
}


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


_PAYMENT_REQUIRED: Final[int] = 402


class _PaymentRequiredReports:
    """Rewrites the report of a test the deployment refused for lack of credits.

    The client maps 400, 401, 403, 404, 409, 422 and 5xx to named exceptions but not 402, so the
    refusal arrives as a bare ApiException holding the server's body.
    """

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        outcome = yield
        report = outcome.get_result()
        excinfo = call.excinfo
        if (
            excinfo is None
            or getattr(excinfo.value, "status", None) != _PAYMENT_REQUIRED
        ):
            return
        host = os.environ.get("OSPARC_API_HOST", "")
        report.longrepr = (
            f"no credits left on {host or 'this deployment'}: it bills this account's wallet, "
            "which cannot pay for the job. Top the wallet up, or run the suite against a "
            "deployment without billing. Balance of the default wallet: "
            "osparc.WalletsApi(api_client).get_default_wallet().available_credits. "
            f"The server answered: {excinfo.value}"
        )


def pytest_terminal_summary(terminalreporter) -> None:
    """Prints deployment, api-server version, client version and result counts after the run."""
    host = os.environ.get("OSPARC_API_HOST", "")
    counts = {
        category: len(terminalreporter.stats.get(category, []))
        for category in ("passed", "failed", "skipped", "error", "xfailed", "xpassed")
    }
    terminalreporter.write_sep("=", "OSPARC e2e: client vs deployment")
    terminalreporter.write_line(
        f"deployment    : {host or 'OSPARC_API_HOST not set'} "
        f"(api-server {_server_api_version(host)})"
    )
    terminalreporter.write_line(
        f"osparc client : {osparc.__version__} "
        f"(labeled {os.environ.get(_CLIENT_VERSION_LABEL_ENV_VAR, 'no')})"
    )
    terminalreporter.write_line(
        "results       : "
        + ", ".join(f"{count} {name}" for name, count in counts.items() if count)
    )


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    _check_client_version_label()
    config.pluginmanager.register(pytest_runtest_setup, "osparc_test_times_plugin")
    config.pluginmanager.register(pytest_runtest_makereport, "osparc_makereport_plugin")
    config.pluginmanager.register(_PaymentRequiredReports(), "osparc_402_plugin")
    config.pluginmanager.register(_e2e_report, "osparc_run_report_plugin")


@pytest.fixture(scope="session")
def api_client() -> Iterable[osparc.ApiClient]:
    # debug=True prints every request and response header, Authorization included, so it is
    # opt-in through OSPARC_E2E_HTTP_DEBUG. The old harness hid it behind pytest > /dev/null.
    http_debug = bool(os.environ.get("OSPARC_E2E_HTTP_DEBUG"))
    if Version(osparc.__version__) >= Version("0.8.0"):
        with osparc.ApiClient() as api_client:
            if http_debug:
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
        if http_debug:
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
    # The basename is unique per run: up to client 0.8.5 upload_file deduplicates on
    # sha256 + filename, so two runs sharing both would be handed one file id and the first
    # teardown to delete it would break the run still using it. The path stays fixed for the
    # whole session, so the re-uploads in test_files_api still exercise within-run dedup.
    tmp_file = (
        tmp_path_factory.mktemp(basename=large_server_file.__name__)
        / f"{large_server_file.__name__}-{uuid4().hex}.txt"
    )
    ss: random.SeedSequence = random.SeedSequence()
    logging.info("Entropy used to generate random file: %s", f"{ss.entropy}")
    rng: random.Generator = random.default_rng(ss)
    tmp_file.write_bytes(rng.bytes(1000))
    # "r+b" opens without truncating, so truncate extends the random prefix with zeros to the
    # full size rather than discarding it the way "wb" did.
    with open(tmp_file, "r+b") as f:
        f.truncate(_file_size)
    assert tmp_file.stat().st_size == _file_size, (
        f"Could not create file of size: {_file_size}"
    )
    ram_statistics, uploaded_file = memory_usage(
        (files_api.upload_file, (tmp_file,)), retval=True
    )
    _record_uploaded_file(uploaded_file.id)

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
    """Newest sleeper release offered by the deployment.

    A deployment chooses which releases to carry, so pinning a version here fails the suite
    wherever that release is missing. Solver.version is SemVer-validated by the generated model,
    so every tag that arrives here orders cleanly.
    """
    releases = osparc.SolversApi(api_client=api_client).list_solver_releases(
        _SLEEPER_KEY
    )
    assert releases, (
        f"{_SLEEPER_KEY} has no release on "
        f"{os.environ.get('OSPARC_API_HOST', 'this deployment')}"
    )
    return max(releases, key=lambda release: Version(release.version))


@pytest.fixture
def sleeper_job_inputs(
    api_client: osparc.ApiClient,
    sleeper: osparc.Solver,
    file_with_number: osparc.File,
) -> osparc.JobInputs:
    """One value for every input port of the release the sleeper fixture picked.

    Input port keys are not stable across sleeper versions (``input1`` in the 2.0.x line,
    ``input_1`` to ``input_4`` in the 2.1.x line, where one of them takes a file), so the values
    follow the release's port metadata rather than a literal from a single version.
    """
    ports = osparc.SolversApi(api_client=api_client).list_solver_ports(
        sleeper.id, sleeper.version
    )
    values: dict[str, Any] = {}
    for port in ports:
        if port.kind != "input":
            continue
        schema: dict[str, Any] = port.content_schema or {}
        if str(schema.get("format", "")).startswith("data:"):
            values[port.key] = file_with_number
        elif "default" in schema:
            values[port.key] = schema["default"]
        else:
            assert schema.get("type") in _INPUT_VALUE_BY_TYPE, (
                f"sleeper {sleeper.version} input port {port.key} has a schema this "
                f"suite knows no value for: {schema}"
            )
            values[port.key] = _INPUT_VALUE_BY_TYPE[schema["type"]]
    assert values, f"sleeper {sleeper.version} offers no input ports"
    return osparc.JobInputs(values)


_TEST_STUDY_TITLE: Final[str] = "sleeper_test_study"

# test_studies.py submits the uploaded file under the first name and expects the job's file back
# under the second.
_TEST_STUDY_INPUT: Final[str] = "input_file"
_TEST_STUDY_OUTPUT: Final[str] = "output_file"


def _study_port_is_named(port: osparc.StudyPort, name: str) -> bool:
    """Whether a study port carries name as its key or as its content schema title.

    The key is the node identifier on newer servers and the label on older ones.
    """
    if port.key == name:
        return True
    schema: dict[str, Any] = port.content_schema or {}
    return schema.get("title") == name


def _describe_study_ports(ports: list[osparc.StudyPort]) -> str:
    described = []
    for port in ports:
        schema: dict[str, Any] = port.content_schema or {}
        described.append(
            f"{port.kind} key={port.key} title={schema.get('title')!r} "
            f"type={schema.get('type')!r} format={schema.get('format')!r}"
        )
    return "; ".join(described) if described else "none"


@pytest.fixture
def sleeper_study_id(api_client: osparc.ApiClient) -> UUID:
    """The deployment's sleeper study, checked before any job uses it.

    The public API can read, clone and run studies but cannot create one, so the study is
    deployment setup. A missing study or port fails with the host and the ports it found.
    """
    study_api = osparc.StudiesApi(api_client=api_client)
    host = os.environ.get("OSPARC_API_HOST", "this deployment")

    def _ensure_uid(study):
        return study.uid if isinstance(study.uid, UUID) else UUID(study.uid)

    matches = [
        study for study in study_api.iter_studies() if study.title == _TEST_STUDY_TITLE
    ]
    if not matches:
        pytest.fail(
            f"no study titled {_TEST_STUDY_TITLE!r} for this account on {host}. The suite "
            f"cannot create it, the public API has no study creation: create it on the "
            f"deployment with a sleeper node exposing its file input as "
            f"{_TEST_STUDY_INPUT!r} and its file output as {_TEST_STUDY_OUTPUT!r}."
        )
    if len(matches) > 1:
        pytest.fail(
            f"{len(matches)} studies titled {_TEST_STUDY_TITLE!r} on {host}: "
            f"{[str(study.uid) for study in matches]}. Keep exactly one for this account."
        )

    study_id = _ensure_uid(matches[0])
    ports: list[osparc.StudyPort] = (
        study_api.list_study_ports(study_id=study_id).items or []
    )
    missing = [
        f"{kind} port {name!r}"
        for name, kind in (
            (_TEST_STUDY_INPUT, "input"),
            (_TEST_STUDY_OUTPUT, "output"),
        )
        if not any(
            port.kind == kind and _study_port_is_named(port, name) for port in ports
        )
    ]
    if missing:
        pytest.fail(
            f"study {_TEST_STUDY_TITLE!r} ({study_id}) on {host} is missing "
            f"{', '.join(missing)}. Ports on it: {_describe_study_ports(ports)}."
        )
    return study_id


@pytest.fixture
def file_with_number(
    tmp_path: Path, api_client: osparc.ApiClient
) -> Iterable[osparc.File]:
    files_api = osparc.FilesApi(api_client=api_client)
    # Unique basename so that, on clients up to 0.8.5 where upload_file deduplicates on
    # sha256 + filename, this run's file is never one another run already uploaded.
    file = tmp_path / f"{file_with_number.__name__}-{uuid4().hex}.txt"
    file.write_text("1")
    server_file = files_api.upload_file(file)
    _record_uploaded_file(server_file.id)
    yield server_file

    try:
        files_api.delete_file(server_file.id)
    except osparc.ApiException:
        _logger.warning(
            f"Could not delete file on server in {file_with_number.__name__}",
            exc_info=True,
        )
