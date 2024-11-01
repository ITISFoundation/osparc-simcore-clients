from osparc import (
    JobMetadata,
    ApiClient,
    SolversApi,
    JobMetadataUpdate,
    JobInputs,
    Job,
    JobOutputs,
)
from faker import Faker
from typing import Callable, Generator
from pydantic import BaseModel
import pytest
from typing import Type, TypeVar

T = TypeVar("T", bound=BaseModel)


@pytest.fixture
def solvers_api(api_client: ApiClient) -> Generator[SolversApi, None, None]:
    yield SolversApi(api_client=api_client)


def test_create_job(
    create_server_mock: Callable[[int, BaseModel], None],
    create_osparc_response_model: Callable,
    solvers_api: SolversApi,
):
    job_inputs = create_osparc_response_model(JobInputs)
    job = create_osparc_response_model(Job)

    create_server_mock(201, job)

    _job = solvers_api.create_job(
        solver_key="mysolver", version="1.2.3", job_inputs=job_inputs
    )
    assert _job == job


def test_get_job_outputs(
    create_server_mock: Callable[[int, BaseModel], None],
    create_osparc_response_model: Callable,
    solvers_api: SolversApi,
    faker: Faker,
):
    job_outputs = create_osparc_response_model(JobOutputs)
    create_server_mock(200, job_outputs)

    _job_outputs = solvers_api.get_job_outputs(
        solver_key="mysolver", version="1.2.3", job_id=faker.uuid4()
    )
    assert _job_outputs == job_outputs


def test_get_job_custom_metadata(
    create_server_mock: Callable[[int, BaseModel], None],
    create_osparc_response_model: Callable[[Type[JobMetadata]], JobMetadata],
    faker: Faker,
    solvers_api: SolversApi,
):
    job_metadata = create_osparc_response_model(JobMetadata)
    create_server_mock(200, job_metadata)

    metadata = solvers_api.get_job_custom_metadata(
        solver_key="mysolver", version="1.2.3", job_id=f"{faker.uuid4()}"
    )
    assert metadata == job_metadata


def test_replace_job_custom_metadata(
    create_server_mock: Callable[[int, BaseModel], None],
    create_osparc_response_model: Callable,
    solvers_api: SolversApi,
    faker: Faker,
):
    job_metadata = create_osparc_response_model(JobMetadata)
    job_metadata_update = create_osparc_response_model(JobMetadataUpdate)
    create_server_mock(200, job_metadata)

    _job_metadata = solvers_api.replace_job_custom_metadata(
        solver_key="mysolver",
        version="1.2.3",
        job_id=f"{faker.uuid4()}",
        job_metadata_update=job_metadata_update,
    )
    assert _job_metadata == job_metadata
