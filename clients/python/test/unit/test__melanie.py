# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument
# pylint: disable=unused-variable
# pylint: disable=too-many-arguments


from pathlib import Path
from typing import List

import osparc
import pytest
from osparc import (
    CreditsApi,
    FilesApi,
    JobInputs,
    JobOutputs,
    JobStatus,
    Solver,
    SolversApi,
    UsersApi,
    WalletsApi,
)


@pytest.fixture
def users_api(api_client: osparc.ApiClient) -> UsersApi:
    return UsersApi(api_client)


@pytest.fixture
def wallets_api(api_client: osparc.ApiClient) -> WalletsApi:
    return WalletsApi(api_client)


@pytest.fixture
def credits_api(api_client: osparc.ApiClient) -> CreditsApi:
    return CreditsApi(api_client)


@pytest.fixture
def files_api(api_client: osparc.ApiClient) -> FilesApi:
    return FilesApi(api_client)


@pytest.fixture
def solvers_api(api_client: osparc.ApiClient) -> SolversApi:
    return SolversApi(api_client)


def test_initialize_solvers(solvers_api: SolversApi):
    # TODO: search a solver and give me all its releases!

    # -> "/{solver_key:path}/releases:search?title='{title}'? or add filter? in list?

    include = {"Sim4Life Python Runner 8.0"}  # titles!?
    # Why not key and we can add a search by release?
    result = []

    # TODO: expose iter_solvers
    for solver in solvers_api.iter_solvers():
        if solver.title in include:
            temp_solver = solvers_api.get_solver_release(
                solver_key=solver.id, version=solver.version
            )
            result[solver.title] = temp_solver

    assert result


def test_upload(files_api: FilesApi, tmp_path: Path):
    p = (tmp_path / "foo.txt").write_text("hi")
    files_api.upload_file(file=p)


# def test_create_run(solvers_api: SolversApi):

#     solvers_api.create_job(
#                 self.solvers_in_use[SolverTitle.S4LPYRUN.value].version,
#                 JobInputs(payloads),
#             )
