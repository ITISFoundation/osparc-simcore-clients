# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument

import os

import osparc
import pytest
from faker import Faker

# aliases of the same setting plus the credentials
_ENV_VAR_NAMES = (
    "OSPARC_API_BASE_URL",
    "OSPARC_API_HOST",
    "OSPARC_API_KEY",
    "OSPARC_API_SECRET",
)

_DEFAULT_HOST = "https://api.osparc.io"


@pytest.fixture
def no_osparc_envs(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in _ENV_VAR_NAMES:
        monkeypatch.delenv(name, raising=False)


@pytest.fixture
def osparc_service_envs(
    monkeypatch: pytest.MonkeyPatch, faker: Faker, no_osparc_envs: None
) -> dict[str, str]:
    # emulate the envs osparc injects when starting a service (e.g. jupyter-math)
    envs = {
        "OSPARC_API_HOST": f"https://api.{faker.safe_domain_name()}",
        "OSPARC_API_KEY": faker.user_name(),
        "OSPARC_API_SECRET": faker.password(length=16),
    }
    for name, value in envs.items():
        monkeypatch.setenv(name, value)
    return envs


def test_defaults_without_envs(no_osparc_envs: None) -> None:
    cfg = osparc.Configuration()
    assert cfg.host == _DEFAULT_HOST
    assert cfg.username is None
    assert cfg.password is None


def test_captures_osparc_envs(osparc_service_envs: dict[str, str]) -> None:
    cfg = osparc.Configuration()
    assert cfg.host == osparc_service_envs["OSPARC_API_HOST"]
    assert cfg.username == osparc_service_envs["OSPARC_API_KEY"]
    assert cfg.password == osparc_service_envs["OSPARC_API_SECRET"]


def test_captures_base_url_alias(
    monkeypatch: pytest.MonkeyPatch, osparc_service_envs: dict[str, str]
) -> None:
    # OSPARC_API_BASE_URL is the service-side name from osparc-simcore#5966
    monkeypatch.delenv("OSPARC_API_HOST")
    monkeypatch.setenv("OSPARC_API_BASE_URL", osparc_service_envs["OSPARC_API_HOST"])
    cfg = osparc.Configuration()
    assert cfg.host == osparc_service_envs["OSPARC_API_HOST"]
    assert cfg.username == osparc_service_envs["OSPARC_API_KEY"]
    assert cfg.password == osparc_service_envs["OSPARC_API_SECRET"]


def test_strips_trailing_slash_from_env_host(
    monkeypatch: pytest.MonkeyPatch, osparc_service_envs: dict[str, str]
) -> None:
    host = osparc_service_envs["OSPARC_API_HOST"]
    monkeypatch.setenv("OSPARC_API_HOST", f"{host}/")
    cfg = osparc.Configuration()
    assert cfg.host == host


def test_explicit_arguments_win_over_envs(
    osparc_service_envs: dict[str, str], faker: Faker
) -> None:
    host = f"https://api.{faker.safe_domain_name()}"
    username = faker.user_name()
    password = faker.password(length=16)
    cfg = osparc.Configuration(host=host, username=username, password=password)
    assert cfg.host == host
    assert cfg.username == username
    assert cfg.password == password


def test_per_field_env_fallback_keeps_explicit_host(
    osparc_service_envs: dict[str, str], faker: Faker
) -> None:
    host = f"https://api.{faker.safe_domain_name()}"
    cfg = osparc.Configuration(host=host)
    assert cfg.host == host
    assert cfg.username == osparc_service_envs["OSPARC_API_KEY"]
    assert cfg.password == osparc_service_envs["OSPARC_API_SECRET"]


def test_partial_envs_fill_only_present_fields(
    monkeypatch: pytest.MonkeyPatch, no_osparc_envs: None, faker: Faker
) -> None:
    monkeypatch.setenv("OSPARC_API_HOST", f"https://api.{faker.safe_domain_name()}")
    monkeypatch.setenv("OSPARC_API_KEY", faker.user_name())
    cfg = osparc.Configuration()
    assert cfg.host == os.environ["OSPARC_API_HOST"]
    assert cfg.username == os.environ["OSPARC_API_KEY"]
    assert cfg.password is None
