import pytest
from pytest_mock import MockerFixture
from osparc import JobMetadata
from faker import Faker


@pytest.fixture
def job_metadata(faker: Faker):
    JobMetadata(job_id=faker.uuid4(), metadata={"int": 2})


def test_job_metadata_serialization(mocker: MockerFixture):
    pass
