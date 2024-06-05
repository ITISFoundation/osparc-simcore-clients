from typing import Iterator

import osparc
import pytest


@pytest.fixture
def cfg() -> Iterator[osparc.Configuration]:
    yield osparc.Configuration(
        host="https://1a52d8d7-9f9f-48e5-b2f0-a226e6b25f0b.com",
        username="askjdg",
        password="asdjbaskjdb",
    )


@pytest.fixture
def enable_dev_mode(monkeypatch):
    monkeypatch.setenv("OSPARC_DEV_FEATURES_ENABLED", "1")
