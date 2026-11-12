# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument

import os
from typing import Final

import osparc
import pytest
from faker import Faker

# the model aliases OSPARC_API_BASE_URL to the same field as OSPARC_API_HOST
_ENV_VAR_NAMES: Final[tuple[str, ...]] = (
    "OSPARC_API_BASE_URL",
    "OSPARC_API_HOST",
    "OSPARC_API_KEY",
    "OSPARC_API_SECRET",
)

_DEFAULT_HOST: Final[str] = "https://api.osparc.io"


@pytest.fixture
def no_osparc_envs(monkeypatch: pytest.MonkeyPatch) -> None:
    """Keep host env vars out of the tests below"""
    for name in _ENV_VAR_NAMES:
        monkeypatch.delenv(name, raising=False)


@pytest.fixture
def osparc_service_envs(
    monkeypatch: pytest.MonkeyPatch, faker: Faker, no_osparc_envs: None
) -> dict[str, str]:
    """Emulate the env vars osparc injects when starting a service"""
    envs = {
        "OSPARC_API_HOST": f"https://api.{faker.safe_domain_name()}",
        "OSPARC_API_KEY": faker.user_name(),
        "OSPARC_API_SECRET": faker.password(length=16),
    }
    for name, value in envs.items():
        monkeypatch.setenv(name, value)
    return envs


def test_defaults_without_envs(no_osparc_envs: None):
    cfg = osparc.Configuration()
    assert cfg.host == _DEFAULT_HOST
    assert cfg.username is None
    assert cfg.password is None


def test_captures_osparc_envs(osparc_service_envs: dict[str, str]):
    cfg = osparc.Configuration()
    assert cfg.host == osparc_service_envs["OSPARC_API_HOST"]
    assert cfg.username == osparc_service_envs["OSPARC_API_KEY"]
    assert cfg.password == osparc_service_envs["OSPARC_API_SECRET"]


def test_captures_base_url_alias(
    monkeypatch: pytest.MonkeyPatch, osparc_service_envs: dict[str, str]
):
    monkeypatch.delenv("OSPARC_API_HOST")
    monkeypatch.setenv("OSPARC_API_BASE_URL", osparc_service_envs["OSPARC_API_HOST"])
    cfg = osparc.Configuration()
    assert cfg.host == osparc_service_envs["OSPARC_API_HOST"]
    assert cfg.username == osparc_service_envs["OSPARC_API_KEY"]
    assert cfg.password == osparc_service_envs["OSPARC_API_SECRET"]


def test_strips_trailing_slash_from_env_host(
    monkeypatch: pytest.MonkeyPatch, osparc_service_envs: dict[str, str]
):
    host = osparc_service_envs["OSPARC_API_HOST"]
    monkeypatch.setenv("OSPARC_API_HOST", f"{host}/")
    cfg = osparc.Configuration()
    assert cfg.host == host


def test_empty_env_vars_are_unset(
    monkeypatch: pytest.MonkeyPatch, osparc_service_envs: dict[str, str]
):
    for name in ("OSPARC_API_HOST", "OSPARC_API_KEY"):
        monkeypatch.setenv(name, "")
    cfg = osparc.Configuration()
    assert cfg.host == _DEFAULT_HOST
    assert cfg.username is None
    assert cfg.password == osparc_service_envs["OSPARC_API_SECRET"]


def test_empty_base_url_does_not_shadow_host_env(
    monkeypatch: pytest.MonkeyPatch, osparc_service_envs: dict[str, str]
):
    monkeypatch.setenv("OSPARC_API_BASE_URL", "")
    cfg = osparc.Configuration()
    assert cfg.host == osparc_service_envs["OSPARC_API_HOST"]


def test_invalid_env_host_does_not_block_explicit_host(
    monkeypatch: pytest.MonkeyPatch, osparc_service_envs: dict[str, str], faker: Faker
):
    monkeypatch.setenv("OSPARC_API_HOST", "not-a-url")
    host = f"https://api.{faker.safe_domain_name()}"
    cfg = osparc.Configuration(host=host)
    assert cfg.host == host
    assert cfg.username == osparc_service_envs["OSPARC_API_KEY"]


def test_explicit_arguments_win_over_envs(
    osparc_service_envs: dict[str, str], faker: Faker
):
    host = f"https://api.{faker.safe_domain_name()}"
    username = faker.user_name()
    secret = faker.password(length=16)
    cfg = osparc.Configuration(host=host, username=username, password=secret)
    assert cfg.host == host
    assert cfg.username == username
    assert cfg.password == secret


def test_per_field_env_fallback_keeps_explicit_host(
    osparc_service_envs: dict[str, str], faker: Faker
):
    host = f"https://api.{faker.safe_domain_name()}"
    cfg = osparc.Configuration(host=host)
    assert cfg.host == host
    assert cfg.username == osparc_service_envs["OSPARC_API_KEY"]
    assert cfg.password == osparc_service_envs["OSPARC_API_SECRET"]


def test_partial_envs_fill_only_present_fields(
    monkeypatch: pytest.MonkeyPatch, no_osparc_envs: None, faker: Faker
):
    monkeypatch.setenv("OSPARC_API_HOST", f"https://api.{faker.safe_domain_name()}")
    monkeypatch.setenv("OSPARC_API_KEY", faker.user_name())
    cfg = osparc.Configuration()
    assert cfg.host == os.environ["OSPARC_API_HOST"]
    assert cfg.username == os.environ["OSPARC_API_KEY"]
    assert cfg.password is None
