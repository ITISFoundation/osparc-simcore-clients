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
from typing import TypeVar

T = TypeVar("T", bound=BaseModel)


@pytest.fixture
def solvers_api(api_client: ApiClient) -> Generator[SolversApi, None, None]:
    yield SolversApi(api_client=api_client)


def test_create_job(
    create_server_mock: Callable[[int], None],
    create_osparc_response_model: Callable,
    solvers_api: SolversApi,
):
    job_inputs = create_osparc_response_model(JobInputs)

    create_server_mock(201)

    _job = solvers_api.create_job(
        solver_key="mysolver", version="1.2.3", job_inputs=job_inputs
    )
    assert isinstance(_job, Job)


def test_get_job_outputs(
    create_server_mock: Callable[[int], None],
    solvers_api: SolversApi,
    faker: Faker,
):
    create_server_mock(200)

    _job_outputs = solvers_api.get_job_outputs(
        solver_key="mysolver", version="1.2.3", job_id=faker.uuid4()
    )
    assert isinstance(_job_outputs, JobOutputs)


def test_get_job_custom_metadata(
    create_server_mock: Callable[[int], None],
    faker: Faker,
    solvers_api: SolversApi,
    create_osparc_response_model: Callable,
):
    _job_metadata = create_osparc_response_model(JobMetadata)
    create_server_mock(200)

    metadata = solvers_api.get_job_custom_metadata(
        solver_key="mysolver", version="1.2.3", job_id=f"{faker.uuid4()}"
    )
    assert isinstance(metadata, JobMetadata)
    assert (
        _job_metadata == metadata
    )  # check fix for https://github.com/ITISFoundation/osparc-simcore/issues/6556


def test_replace_job_custom_metadata(
    create_server_mock: Callable[[int], None],
    create_osparc_response_model: Callable,
    solvers_api: SolversApi,
    faker: Faker,
):
    job_metadata = create_osparc_response_model(JobMetadata)
    job_metadata_update = create_osparc_response_model(JobMetadataUpdate)
    create_server_mock(200)

    _job_metadata = solvers_api.replace_job_custom_metadata(
        solver_key="mysolver",
        version="1.2.3",
        job_id=f"{faker.uuid4()}",
        job_metadata_update=job_metadata_update,
    )
    assert isinstance(_job_metadata, JobMetadata)
    assert (
        _job_metadata == job_metadata
    )  # check fix for https://github.com/ITISFoundation/osparc-simcore/issues/6556
