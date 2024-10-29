import pytest
from osparc import JobMetadata, ApiClient, SolversApi, JobMetadataUpdate
from faker import Faker
from typing import Callable
from pydantic import BaseModel


@pytest.fixture
def job_metadata(faker: Faker) -> JobMetadata:
    _job_id = f"{faker.uuid4()}"
    return JobMetadata(
        job_id=_job_id,
        metadata={
            "job_id": _job_id,
            "job_name": f"{faker.text()}",
            "node_id": f"{faker.uuid4()}",
        },
        url=faker.url(),
    )


@pytest.fixture
def job_metadata_update(faker: Faker):
    return JobMetadataUpdate(
        metadata={
            "var1": faker.boolean(),
            "var2": faker.pyfloat(),
            "var3": faker.pyint(),
            "var4": faker.text(),
        }
    )


def test_get_job_custom_metadata(
    create_server_mock: Callable[[int, BaseModel], None],
    job_metadata: JobMetadata,
    api_client: ApiClient,
    faker: Faker,
):
    create_server_mock(200, job_metadata)

    _solvers_api = SolversApi(api_client=api_client)
    metadata = _solvers_api.get_job_custom_metadata(
        solver_key="mysolver", version="1.2.3", job_id=f"{faker.uuid4()}"
    )
    assert metadata == job_metadata
