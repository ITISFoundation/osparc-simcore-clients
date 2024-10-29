from osparc import JobMetadata, ApiClient, SolversApi, JobMetadataUpdate
from faker import Faker
from typing import Callable
from pydantic import BaseModel


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


def test_replace_job_custom_metadata(
    create_server_mock: Callable[[int, BaseModel], None],
    job_metadata: JobMetadata,
    job_metadata_update: JobMetadataUpdate,
    api_client: ApiClient,
    faker: Faker,
):
    create_server_mock(200, job_metadata)

    _solvers_api = SolversApi(api_client=api_client)
    _job_metadata = _solvers_api.replace_job_custom_metadata(
        solver_key="mysolver",
        version="1.2.3",
        job_id=f"{faker.uuid4()}",
        job_metadata_update=job_metadata_update,
    )
    assert _job_metadata == job_metadata
