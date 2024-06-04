import os

import pytest
from osparc import SolversApi, StudiesApi
from osparc._models import ParentProjectInfo


@pytest.mark.parametrize("parent_headers", [True, False])
def test_create_jobs_parent_headers(
    mocker, faker, enable_dev_mode, parent_headers: bool
):
    def check_headers(**kwargs):
        parent_info = ParentProjectInfo()
        if parent_headers:
            assert parent_info.x_simcore_parent_project_uuid is not None
            assert parent_info.x_simcore_parent_node_id is not None
            assert parent_info.x_simcore_parent_project_uuid == kwargs.get(
                "x_simcore_parent_project_uuid"
            )
            assert parent_info.x_simcore_parent_node_id == kwargs.get(
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

    if parent_headers:
        os.environ["OSPARC_STUDY_ID"] = f"{faker.uuid4()}"
        os.environ["OSPARC_NODE_ID"] = f"{faker.uuid4()}"

    solvers_api = SolversApi()
    solvers_api.create_job(solver_key="mysolver", version="1.2.3", job_inputs={})

    studies_api = StudiesApi()
    studies_api.create_study_job(study_id=faker.uuid4(), job_inputs={})
    studies_api.clone_study(study_id=faker.uuid4())