import os
from typing import Callable

import pytest
from osparc import SolversApi, StudiesApi


@pytest.fixture
def create_parent_env(monkeypatch, faker) -> Callable[[bool], None]:
    def _(enable: bool):
        if enable:
            monkeypatch.setenv("OSPARC_STUDY_ID", f"{faker.uuid4()}")
            monkeypatch.setenv("OSPARC_NODE_ID", f"{faker.uuid4()}")

    yield _


@pytest.mark.parametrize("parent_env", [True, False])
def test_create_jobs_parent_headers(
    mocker, faker, create_parent_env, enable_dev_mode, parent_env: bool
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
