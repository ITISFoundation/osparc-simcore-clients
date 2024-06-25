import osparc
import pytest
from faker import Faker

@pytest.fixture
def cfg(faker: Faker) -> osparc.Configuration:
    return osparc.Configuration(
        host="https://1a52d8d7-9f9f-48e5-b2f0-a226e6b25f0b.com",
        username=faker.user_name(),
        password=faker.password(),
    )


@pytest.fixture
def enable_dev_mode(monkeypatch:pytest.MonkeyPatch):
    monkeypatch.setenv("OSPARC_DEV_FEATURES_ENABLED", "1")
