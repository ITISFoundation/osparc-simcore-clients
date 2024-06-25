import datetime
import logging
import os
from pathlib import Path
from typing import Iterable

import osparc
import pytest
from httpx import AsyncClient, BasicAuth
from numpy import random
from pydantic import ByteSize

_KB: ByteSize = ByteSize(1024)  # in bytes
_MB: ByteSize = ByteSize(_KB * 1024)  # in bytes
_GB: ByteSize = ByteSize(_MB * 1024)  # in bytes


# Dictionary to store start times of tests
_test_start_times = {}


def _utc_now():
    return datetime.datetime.now(tz=datetime.timezone.utc)


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


def pytest_runtest_setup(item):
    """
    Hook to capture the start time of each test.
    """
    _test_start_times[item.name] = _utc_now()


def pytest_runtest_makereport(item, call):
    """
    Hook to add extra information when a test fails.
    """
    if call.when == "call":

        # Check if the test failed
        if call.excinfo is not None:
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
                diagnostics["graylog_url"] = _construct_graylog_url(api_host, start_time, end_time)

            # Print the diagnostics
            print(f"\nDiagnostics for {test_name}:")
            for key, value in diagnostics.items():
                print("  ", key, ":", value)


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    config.pluginmanager.register(pytest_runtest_setup, "osparc_test_times_plugin")
    config.pluginmanager.register(pytest_runtest_makereport, "osparc_makereport_plugin")


@pytest.fixture
def configuration() -> Iterable[osparc.Configuration]:
    assert (host := os.environ.get("OSPARC_API_HOST"))
    assert (username := os.environ.get("OSPARC_API_KEY"))
    assert (password := os.environ.get("OSPARC_API_SECRET"))
    yield osparc.Configuration(
        host=host,
        username=username,
        password=password,
    )


@pytest.fixture
def api_client(configuration: osparc.Configuration) -> Iterable[osparc.ApiClient]:
    with osparc.ApiClient(configuration=configuration) as api_client:
        yield api_client


@pytest.fixture
def async_client(configuration) -> Iterable[AsyncClient]:
    yield AsyncClient(
        base_url=configuration.host,
        auth=BasicAuth(
            username=configuration.username, password=configuration.password
        ),
    )  # type: ignore


@pytest.fixture
def tmp_file(tmp_path: Path, caplog) -> Path:
    caplog.set_level(logging.INFO)
    byte_size: ByteSize = 1 * _GB
    tmp_file = tmp_path / "large_test_file.txt"
    ss: random.SeedSequence = random.SeedSequence()
    logging.info("Entropy used to generate random file: %s", f"{ss.entropy}")
    rng: random.Generator = random.default_rng(ss)
    tmp_file.write_bytes(rng.bytes(1000))
    with open(tmp_file, "wb") as f:
        f.truncate(byte_size)
    assert (
        tmp_file.stat().st_size == byte_size
    ), f"Could not create file of size: {byte_size}"
    return tmp_file


@pytest.fixture
def sleeper(api_client: osparc.ApiClient) -> osparc.Solver:
    solvers_api = osparc.SolversApi(api_client=api_client)
    sleeper: osparc.Solver = solvers_api.get_solver_release(
        "simcore/services/comp/itis/sleeper", "2.0.2"
    )  # type: ignore
    return sleeper
