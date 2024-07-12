import os
from typing import Callable, Optional

import pytest
from faker import Faker
from osparc import ApiClient, SolversApi, StudiesApi
from pytest_mock import MockerFixture


@pytest.fixture
def create_parent_env(
    monkeypatch: pytest.MonkeyPatch, faker: Faker
) -> Callable[[bool], None]:
    def _(enable: bool):
        if enable:
            monkeypatch.setenv("OSPARC_STUDY_ID", f"{faker.uuid4()}")
            monkeypatch.setenv("OSPARC_NODE_ID", f"{faker.uuid4()}")

    return _


@pytest.mark.parametrize("parent_env", [True, False])
def test_create_jobs_parent_headers(
    mocker: MockerFixture,
    faker: Faker,
    create_parent_env: Callable,
    dev_mode_enabled: None,
    parent_env: bool,
):
    create_parent_env(parent_env)

    def check_headers(**kwargs):
        if parent_env:
            assert os.environ["OSPARC_STUDY_ID"] == kwargs.get(
                "x_simcore_parent_project_uuid"
            )
            assert os.environ["OSPARC_NODE_ID"] == kwargs.get(
                "x_simcore_parent_node_id"
            )

    mocker.patch(
        "osparc_client.SolversApi.create_job",
        side_effect=lambda solver_key, version, job_inpus, **kwargs: check_headers(
            **kwargs
        ),
    )
    mocker.patch(
        "osparc_client.StudiesApi.create_study_job",
        side_effect=lambda study_id, job_inputs, **kwargs: check_headers(**kwargs),
    )
    mocker.patch(
        "osparc_client.StudiesApi.clone_study",
        side_effect=lambda study_id, **kwargs: check_headers(**kwargs),
    )

    solvers_api = SolversApi()
    solvers_api.create_job(solver_key="mysolver", version="1.2.3", job_inputs={})

    studies_api = StudiesApi()
    studies_api.create_study_job(study_id=faker.uuid4(), job_inputs={})
    studies_api.clone_study(study_id=faker.uuid4())


@pytest.mark.parametrize(
    "OSPARC_API_HOST", ["https://api.foo.com", "https://api.bar.com/", None]
)
@pytest.mark.parametrize("OSPARC_API_KEY", ["key", None])
@pytest.mark.parametrize("OSPARC_API_SECRET", ["secret", None])
def test_api_client_constructor(
    monkeypatch: pytest.MonkeyPatch,
    OSPARC_API_HOST: Optional[str],
    OSPARC_API_KEY: Optional[str],
    OSPARC_API_SECRET: Optional[str],
):
    with monkeypatch.context() as patch:
        patch.delenv("OSPARC_API_HOST", raising=False)
        patch.delenv("OSPARC_API_KEY", raising=False)
        patch.delenv("OSPARC_API_SECRET", raising=False)

        if OSPARC_API_HOST is not None:
            patch.setenv("OSPARC_API_HOST", OSPARC_API_HOST)
        if OSPARC_API_KEY is not None:
            patch.setenv("OSPARC_API_KEY", OSPARC_API_KEY)
        if OSPARC_API_SECRET is not None:
            patch.setenv("OSPARC_API_SECRET", OSPARC_API_SECRET)

        if OSPARC_API_HOST and OSPARC_API_KEY and OSPARC_API_SECRET:
            api = ApiClient()
            assert api.configuration.host == OSPARC_API_HOST.rstrip("/")
            assert api.configuration.username == OSPARC_API_KEY
            assert api.configuration.password == OSPARC_API_SECRET

        else:
            with pytest.raises(RuntimeError):
                ApiClient()
