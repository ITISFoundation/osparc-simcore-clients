import pytest
from osparc import (
    ApiClient,
    StudiesApi,
    JobInputs,
    Job,
    JobOutputs,
    JobMetadata,
    JobMetadataUpdate,
)
from typing import Callable
from faker import Faker


@pytest.fixture
def studies_api(api_client: ApiClient) -> StudiesApi:
    return StudiesApi(api_client=api_client)


def test_create_study_job(
    create_server_mock: Callable[[int], None],
    create_osparc_response_model: Callable,
    studies_api: StudiesApi,
    faker: Faker,
):
    job_inputs = create_osparc_response_model(JobInputs)

    create_server_mock(200)

    _job = studies_api.create_study_job(study_id=faker.uuid4(), job_inputs=job_inputs)
    assert isinstance(_job, Job)


def test_get_study_job_outputs(
    create_server_mock: Callable[[int], None], studies_api: StudiesApi, faker: Faker
):
    create_server_mock(200)

    _study_job_outputs = studies_api.get_study_job_outputs(
        study_id=faker.uuid4(), job_id=faker.uuid4()
    )
    assert isinstance(_study_job_outputs, JobOutputs)


def test_get_study_job_custom_metadata(
    create_server_mock: Callable[[int], None], studies_api: StudiesApi, faker: Faker
):
    create_server_mock(200)
    metadata = studies_api.get_study_job_custom_metadata(
        study_id=faker.uuid4(), job_id=faker.uuid4()
    )
    assert isinstance(metadata, JobMetadata)


def test_replace_study_job_custom_metadata(
    create_server_mock: Callable[[int], None],
    create_osparc_response_model: Callable,
    studies_api: StudiesApi,
    faker: Faker,
):
    job_metadata_update: JobMetadataUpdate = create_osparc_response_model(
        JobMetadataUpdate
    )
    job_metadata = studies_api.replace_study_job_custom_metadata(
        study_id=faker.uuid4(),
        job_id=faker.uuid4(),
        job_metadata_update=job_metadata_update,
    )
    assert isinstance(job_metadata, JobMetadata)
