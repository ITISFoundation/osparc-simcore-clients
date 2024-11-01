# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument
# pylint: disable=unused-variable
# pylint: disable=too-many-arguments

import osparc
import pytest
from faker import Faker
from pytest_mock import MockerFixture
from urllib3 import HTTPResponse
from pydantic import BaseModel
from typing import Callable, Generator
from prance import ResolvingParser
import json
from tempfile import NamedTemporaryFile
from pathlib import Path
from typing import Any, Type, TypeVar


@pytest.fixture
def cfg(faker: Faker) -> osparc.Configuration:
    return osparc.Configuration(
        host=f"https://api.{faker.safe_domain_name()}",
        username=faker.user_name(),
        password=faker.password(),
    )


@pytest.fixture
def osparc_openapi_specs() -> Generator[dict[str, Any], None, None]:
    with NamedTemporaryFile(suffix=".json") as file:
        file = Path(file.name)
        file.write_text(json.dumps(osparc.openapi()))
        osparc_spec = ResolvingParser(f"{file.resolve()}").specification
    assert osparc_spec is not None
    yield osparc_spec


@pytest.fixture
def api_client(cfg: osparc.Configuration) -> osparc.ApiClient:
    return osparc.ApiClient(configuration=cfg)


@pytest.fixture
def dev_mode_enabled(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OSPARC_DEV_FEATURES_ENABLED", "1")


@pytest.fixture
def create_server_mock(
    mocker: MockerFixture,
) -> Generator[Callable[[int, BaseModel], None], None, None]:
    def _mock_server(_status: int, _body: BaseModel) -> None:
        def _sideeffect(
            method: str,
            url: str,
            body=None,
            fields=None,
            headers=None,
            json=None,
            **urlopen_kw,
        ) -> HTTPResponse:
            response = HTTPResponse(
                status=_status, body=_body.model_dump_json().encode()
            )
            return response

        mocker.patch("urllib3.PoolManager.request", side_effect=_sideeffect)

    yield _mock_server


T = TypeVar("T", bound=BaseModel)


@pytest.fixture
def create_osparc_response_model(
    osparc_openapi_specs: dict[str, Any],
) -> Generator[Callable[[Type[T]], T], None, None]:
    def _create_model(model_type: Type[T]) -> T:
        schemas = osparc_openapi_specs.get("components", {}).get("schemas", {})
        example_data = schemas.get(model_type.__name__, {}).get("example", {})
        assert example_data, (
            "Could not extract example data for",
            " '{model_type.__name__}' from openapi specs",
        )
        return model_type.model_validate(example_data)

    yield _create_model
