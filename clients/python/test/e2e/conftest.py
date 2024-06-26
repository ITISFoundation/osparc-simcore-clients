# pylint: disable=protected-access
# pylint: disable=redefined-outer-name
# pylint: disable=too-many-arguments
# pylint: disable=unused-argument
# pylint: disable=unused-variable

import logging
import os
from pathlib import Path
from typing import Iterable
from uuid import UUID

import osparc
import pytest
from httpx import AsyncClient, BasicAuth
from numpy import random
from pydantic import ByteSize

_KB: ByteSize = ByteSize(1024)  # in bytes
_MB: ByteSize = ByteSize(_KB * 1024)  # in bytes
_GB: ByteSize = ByteSize(_MB * 1024)  # in bytes


@pytest.fixture
def configuration() -> osparc.Configuration:
    assert (host := os.environ.get("OSPARC_API_HOST"))
    assert (username := os.environ.get("OSPARC_API_KEY"))
    assert (password := os.environ.get("OSPARC_API_SECRET"))
    return osparc.Configuration(
        host=host,
        username=username,
        password=password,
    )


@pytest.fixture
def api_client(configuration: osparc.Configuration) -> Iterable[osparc.ApiClient]:
    with osparc.ApiClient(configuration=configuration) as _api_client:
        yield _api_client


@pytest.fixture
def async_client(configuration: osparc.Configuration) -> AsyncClient:
    return AsyncClient(
        base_url=configuration.host,
        auth=BasicAuth(
            username=configuration.username, password=configuration.password
        ),
    )  # type: ignore


@pytest.fixture
def tmp_file(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> Path:
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


@pytest.fixture
def sleeper_study_id(api_client: osparc.ApiClient) -> UUID:
    """Simple sleeper study template which takes
    as input a single file containing a single integer"""
    _test_study_title = "sleeper_test_study"
    study_api = osparc.StudiesApi(api_client=api_client)
    for study in study_api.studies():
        if study.title == _test_study_title:
            return UUID(study.uid)
    pytest.fail(f"Could not find {_test_study_title} study")


@pytest.fixture
def file_with_number(
    tmp_path: Path, api_client: osparc.ApiClient
) -> Iterable[osparc.File]:
    files_api = osparc.FilesApi(api_client=api_client)
    file = tmp_path / "file_with_number.txt"
    file.write_text("1")
    server_file = files_api.upload_file(file)
    yield server_file

    files_api.delete_file(server_file.id)
