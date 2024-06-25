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
def dev_mode_enabled(monkeypatch:pytest.MonkeyPatch):
    monkeypatch.setenv("OSPARC_DEV_FEATURES_ENABLED", "1")
