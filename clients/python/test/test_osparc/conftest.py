# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument
# pylint: disable=unused-variable
# pylint: disable=too-many-arguments

import osparc
import pytest
from faker import Faker


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
def page_file(faker: Faker) -> osparc.PageFile:
    items = []
    for _ in range(5):
        items.append(
            osparc.File(
                id=faker.uuid4(),
                filename=faker.file_name(),
                content_type=None,
                checksum=faker.sha256(),
                e_tag=faker.sha256(),
            )
        )

    return osparc.PageFile(
        items=items,
        total=faker.pyint(min_value=1, max_value=10) * len(items),
        limit=len(items),
        offset=faker.pyint(min_value=0),
        links=osparc.Links(next=faker.url()),
    )
