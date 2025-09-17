# pylint: disable=protected-access
# pylint: disable=redefined-outer-name
# pylint: disable=too-many-arguments
# pylint: disable=unused-argument
# pylint: disable=unused-variable

import json

import osparc
from _utils import skip_if_osparc_version
from httpx import AsyncClient
from packaging.version import Version
from uuid import UUID

DEFAULT_TIMEOUT_SECONDS = 10 * 60  # 10 min


@skip_if_osparc_version(at_least=Version("0.8.3.post0.dev20"))
def test_jobs(api_client: osparc.ApiClient, sleeper: osparc.Solver):
    """Test the jobs method

    Args:
        configuration (osparc.Configuration): The Configuration
    """
    n_jobs: int = 3
    solvers_api = osparc.SolversApi(api_client=api_client)
    # initial iterator
    init_iter = solvers_api.iter_jobs(sleeper.id, sleeper.version)
    n_init_iter: int = len(init_iter)
    assert n_init_iter >= 0

    # create n_jobs jobs
    created_job_ids = []
    for _ in range(n_jobs):
        job: osparc.Job = solvers_api.create_job(
            sleeper.id, sleeper.version, osparc.JobInputs({"input1": 1.0})
        )
        created_job_ids.append(job.id)

    tmp_iter = solvers_api.iter_jobs(sleeper.id, sleeper.version)
    solvers_api.iter_jobs(sleeper.id, sleeper.version)

    final_iter = solvers_api.iter_jobs(sleeper.id, sleeper.version)
    assert len(final_iter) > 0, "No jobs were available"
    assert n_init_iter + n_jobs == len(
        final_iter
    ), "An incorrect number of jobs was recorded"

    for ii, elm in enumerate(tmp_iter):
        assert isinstance(elm, osparc.Job)
        if ii > 100:
            break

    # cleanup
    for elm in created_job_ids:
        solvers_api.delete_job(sleeper.id, sleeper.version, elm)


@skip_if_osparc_version(at_least=Version("0.6.5"))
async def test_logstreaming(
    api_client: osparc.ApiClient, sleeper: osparc.Solver, async_client: AsyncClient
):
    """Test log streaming"""
    solvers_api: osparc.SolversApi = osparc.SolversApi(api_client)
    job: osparc.Job = solvers_api.create_job(
        sleeper.id, sleeper.version, osparc.JobInputs({"input1": 1.0})
    )  # type: ignore

    solvers_api.start_job(sleeper.id, sleeper.version, job.id)

    nloglines: int = 0
    url = f"/v0/solvers/{sleeper.id}/releases/{sleeper.version}/jobs/{job.id}/logstream"
    print(f"starting logstreaming from {url}...")

    async with async_client.stream(
        "GET",
        url,
        timeout=DEFAULT_TIMEOUT_SECONDS,
    ) as response:
        async for line in response.aiter_lines():
            log = json.loads(line)
            job_id = log.get("job_id")
            assert job_id
            assert job_id == (
                f"{job.id}" if isinstance(job.id, UUID) else job.id
            )  # keep test backwards compatible
            nloglines += 1
            print("\n".join(log.get("messages")))
            if nloglines > 10:  # dont wait too long
                await response.aclose()
                break

    assert nloglines > 0, f"Could not stream log for {sleeper.id=}, \
        {sleeper.version=} and {job.id=}"  # type: ignore
    solvers_api.delete_job(sleeper.id, sleeper.version, job.id)
