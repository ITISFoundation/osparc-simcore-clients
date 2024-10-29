# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument
# pylint: disable=unused-variable
# pylint: disable=too-many-arguments

import osparc
import pytest
from faker import Faker
from pytest_mock import MockerFixture
from urllib3 import HTTPResponse
from pydantic import BaseModel
from typing import Callable, Generator


@pytest.fixture
def cfg(faker: Faker) -> osparc.Configuration:
    return osparc.Configuration(
        host=f"https://api.{faker.safe_domain_name()}",
        username=faker.user_name(),
        password=faker.password(),
    )


@pytest.fixture
def api_client(cfg: osparc.Configuration) -> osparc.ApiClient:
    return osparc.ApiClient(configuration=cfg)


@pytest.fixture
def dev_mode_enabled(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OSPARC_DEV_FEATURES_ENABLED", "1")


@pytest.fixture
def create_server_mock(
    mocker: MockerFixture,
) -> Generator[Callable[[int, BaseModel], None], None, None]:
    def _mock_server(_status: int, _body: BaseModel) -> None:
        def _sideeffect(
            method: str,
            url: str,
            body=None,
            fields=None,
            headers=None,
            json=None,
            **urlopen_kw,
        ) -> HTTPResponse:
            response = HTTPResponse(
                status=_status, body=_body.model_dump_json().encode()
            )
            return response

        mocker.patch("urllib3.PoolManager.request", side_effect=_sideeffect)

    yield _mock_server


@pytest.fixture
def job_metadata_update(faker: Faker):
    return osparc.JobMetadataUpdate(
        metadata={
            "boolean": faker.boolean(),
            "float": faker.pyfloat(),
            "int": faker.pyint(),
            "str": faker.text(),
            "None": None,
        }
    )


@pytest.fixture
def job_metadata(
    faker: Faker, job_metadata_update: osparc.JobMetadataUpdate
) -> osparc.JobMetadata:
    return osparc.JobMetadata(
        job_id=f"{faker.uuid4()}",
        metadata=job_metadata_update.metadata,
        url=faker.url(),
    )


@pytest.fixture
def job_inputs(faker: Faker) -> osparc.JobInputs:
    return osparc.JobInputs(
        {
            "File": osparc.File(id=f"{faker.uuid4()}", filename=faker.file_name()),
            "bool": faker.boolean(),
            "float": faker.pyfloat(),
            "int": faker.pyint(),
            "str": faker.text(),
            "None": None,
        }
    )


@pytest.fixture
def job(faker: Faker) -> osparc.Job:
    return osparc.Job(
        id=f"{faker.uuid4()}",
        name=faker.file_name(),
        inputs_checksum=f"{faker.sha256()}",
        created_at=faker.date_time(),
        runner_name="runner1",  # must validate regexp, hence hardcoded
        url=None,
        runner_url=None,
        outputs_url=None,
    )
