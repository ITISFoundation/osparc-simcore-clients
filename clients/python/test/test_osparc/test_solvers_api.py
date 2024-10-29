from osparc import JobMetadata, ApiClient, SolversApi, JobMetadataUpdate, JobInputs, Job
from faker import Faker
from typing import Callable, Generator
from pydantic import BaseModel
import pytest


@pytest.fixture
def solvers_api(api_client: ApiClient) -> Generator[SolversApi, None, None]:
    yield SolversApi(api_client=api_client)


def test_create_job(
    create_server_mock: Callable[[int, BaseModel], None],
    job_inputs: JobInputs,
    job: Job,
    solvers_api: SolversApi,
):
    create_server_mock(201, job)

    _job = solvers_api.create_job(
        solver_key="mysolver", version="1.2.3", job_inputs=job_inputs
    )
    assert _job == job


def test_get_job_custom_metadata(
    create_server_mock: Callable[[int, BaseModel], None],
    job_metadata: JobMetadata,
    faker: Faker,
    solvers_api: SolversApi,
):
    create_server_mock(200, job_metadata)

    metadata = solvers_api.get_job_custom_metadata(
        solver_key="mysolver", version="1.2.3", job_id=f"{faker.uuid4()}"
    )
    assert metadata == job_metadata


def test_replace_job_custom_metadata(
    create_server_mock: Callable[[int, BaseModel], None],
    job_metadata: JobMetadata,
    job_metadata_update: JobMetadataUpdate,
    solvers_api: SolversApi,
    faker: Faker,
):
    create_server_mock(200, job_metadata)

    _job_metadata = solvers_api.replace_job_custom_metadata(
        solver_key="mysolver",
        version="1.2.3",
        job_id=f"{faker.uuid4()}",
        job_metadata_update=job_metadata_update,
    )
    assert _job_metadata == job_metadata
