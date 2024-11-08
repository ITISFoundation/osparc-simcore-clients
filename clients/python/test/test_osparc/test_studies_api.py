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


@pytest.fixture
def studies_api(api_client: ApiClient) -> StudiesApi:
    return StudiesApi(api_client=api_client)


def test_create_study_job(
    create_server_mock: Callable[[int], None],
    create_osparc_response_model: Callable,
    studies_api: StudiesApi,
    uuid: str,
):
    job_inputs = create_osparc_response_model(JobInputs)

    create_server_mock(200)

    _job = studies_api.create_study_job(study_id=uuid, job_inputs=job_inputs)
    assert isinstance(_job, Job)


def test_get_study_job_outputs(
    create_server_mock: Callable[[int], None], studies_api: StudiesApi, uuid: str
):
    create_server_mock(200)

    _study_job_outputs = studies_api.get_study_job_outputs(study_id=uuid, job_id=uuid)
    assert isinstance(_study_job_outputs, JobOutputs)


def test_get_study_job_custom_metadata(
    create_osparc_response_model: Callable,
    create_server_mock: Callable[[int], None],
    studies_api: StudiesApi,
    uuid: str,
):
    _job_metadata: JobMetadata = create_osparc_response_model(JobMetadata)
    create_server_mock(200)
    metadata = studies_api.get_study_job_custom_metadata(study_id=uuid, job_id=uuid)
    assert isinstance(metadata, JobMetadata)
    assert (
        _job_metadata == metadata
    )  # check fix for https://github.com/ITISFoundation/osparc-simcore/issues/6556


def test_replace_study_job_custom_metadata(
    create_server_mock: Callable[[int], None],
    create_osparc_response_model: Callable,
    studies_api: StudiesApi,
    uuid: str,
):
    create_server_mock(200)
    _job_metadata: JobMetadata = create_osparc_response_model(JobMetadata)
    job_metadata_update: JobMetadataUpdate = create_osparc_response_model(
        JobMetadataUpdate
    )
    job_metadata = studies_api.replace_study_job_custom_metadata(
        study_id=uuid,
        job_id=uuid,
        job_metadata_update=job_metadata_update,
    )
    assert isinstance(job_metadata, JobMetadata)
    assert (
        _job_metadata == job_metadata
    )  # check fix for https://github.com/ITISFoundation/osparc-simcore/issues/6556
