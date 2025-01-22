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
from typing import Any, TypeVar, NamedTuple, Final, cast, Dict, Type, Set
from urllib.parse import urlparse
from parse import parse, with_pattern


@pytest.fixture
def cfg(faker: Faker) -> osparc.Configuration:
    return osparc.Configuration(
        host=f"https://api.{faker.safe_domain_name()}",
        username=faker.user_name(),
        password=faker.password(),
    )


@pytest.fixture
def osparc_openapi_specs() -> Generator[Dict[str, Any], None, None]:
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
def uuid(faker: Faker):
    return cast(str, faker.uuid4())


@pytest.fixture
def dev_mode_enabled(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OSPARC_DEV_FEATURES_ENABLED", "1")


@with_pattern(pattern=r"[^/]+")
def _path_segment(text):
    return text


class ServerPath(NamedTuple):
    path: str
    formatted_path: str


_PATH_SEGMENT_CONVERTER: Final[str] = "path_segment"


@pytest.fixture
def all_server_paths(osparc_openapi_specs: Dict[str, Any]) -> Set[ServerPath]:
    server_paths = set()
    for path in osparc_openapi_specs["paths"]:
        for method in osparc_openapi_specs["paths"][path]:
            if params := osparc_openapi_specs["paths"][path][method].get("parameters"):
                formatted_path = path
                for p in params:
                    pname = p.get("name")
                    assert pname is not None
                    formatted_path = formatted_path.replace(
                        "{" + f"{pname}" + "}",
                        "{" + f"{pname}:{_PATH_SEGMENT_CONVERTER}" + "}",
                    )
                server_paths.add(ServerPath(path=path, formatted_path=formatted_path))
    return server_paths


T = TypeVar("T", bound=BaseModel)


@pytest.fixture
def create_osparc_response_model(
    osparc_openapi_specs: Dict[str, Any],
) -> Callable[[Type[T]], T]:
    def _create_model(model_type: Type[T]) -> T:
        schemas = osparc_openapi_specs.get("components", {}).get("schemas", {})
        example_data = schemas.get(model_type.__name__, {}).get("example")
        error_msg = "Could not extract example data for"
        error_msg += f" '{model_type.__name__}' from openapi specs"
        assert example_data, error_msg
        return model_type.model_validate(example_data)

    return _create_model


@pytest.fixture
def create_server_mock(
    mocker: MockerFixture,
    osparc_openapi_specs: Dict[str, Any],
    all_server_paths: Set[ServerPath],
    create_osparc_response_model: Callable[[str], BaseModel],
) -> Callable[[int], None]:
    def _mock_server(_status: int) -> None:
        def _sideeffect(
            method: str,
            url: str,
            body=None,
            fields=None,
            headers=None,
            json=None,
            **urlopen_kw,
        ) -> HTTPResponse:
            matching_paths = set(
                p.path
                for p in all_server_paths
                if parse(
                    p.formatted_path,
                    urlparse(url=url).path,
                    {_PATH_SEGMENT_CONVERTER: _path_segment},
                )
            )
            assert len(matching_paths) == 1
            matching_path = list(matching_paths)[0]
            responses = (
                osparc_openapi_specs["paths"]
                .get(matching_path, {})
                .get(method.lower(), {})
                .get("responses")
            )
            assert responses is not None
            schema = (
                responses.get(f"{_status}", {})
                .get("content", {})
                .get("application/json", {})
                .get("schema")
            )
            assert (
                schema is not None
            ), f"probably status code {_status} is not a return code of {method.upper()} {matching_path}"
            response_model_type = getattr(osparc, schema.get("title"))
            response_model = create_osparc_response_model(response_model_type)
            response = HTTPResponse(
                status=_status, body=response_model.model_dump_json().encode()
            )
            return response

        mocker.patch("urllib3.PoolManager.request", side_effect=_sideeffect)

    return _mock_server


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
        total=faker.pyint(min_value=len(items) + 1, max_value=len(items) + 100),
        limit=len(items),
        offset=faker.pyint(min_value=0),
        links=osparc.Links(
            first=faker.url(),
            last=faker.url(),
            next=faker.url(),
            prev=faker.url(),
            self=faker.url(),
        ),
    )
