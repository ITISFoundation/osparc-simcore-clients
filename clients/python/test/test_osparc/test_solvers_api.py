import pytest
from pytest_mock import MockerFixture
from osparc import JobMetadata, MetadataValue, ApiClient, SolversApi
from faker import Faker
from urllib3 import HTTPResponse


@pytest.fixture
def job_metadata(faker: Faker) -> JobMetadata:
    _job_id = faker.uuid4()
    return JobMetadata(
        job_id=f"{_job_id}",
        metadata={
            "job_id": MetadataValue(_job_id),
            "job_name": MetadataValue(faker.text()),
            "node_id": MetadataValue(faker.uuid4()),
        },
        url=faker.url(),
    )


def test_job_metadata_serialization(
    mocker: MockerFixture,
    job_metadata: JobMetadata,
    api_client: ApiClient,
    faker: Faker,
):
    def _get_job_sideeffect(
        method: str,
        url: str,
        body=None,
        fields=None,
        headers=None,
        json=None,
        **urlopen_kw,
    ) -> HTTPResponse:
        response = HTTPResponse(status=200, body=job_metadata.to_json().encode())
        return response

    mocker.patch("urllib3.PoolManager.request", side_effect=_get_job_sideeffect)

    _solvers_api = SolversApi(api_client=api_client)
    metadata = _solvers_api.get_job_custom_metadata(
        solver_key="mysolver", version="1.2.3", job_id=f"{faker.uuid4()}"
    )
    print(metadata)
