import logging

import osparc
from _utils import requires_dev_features
from httpx import AsyncClient, BasicAuth

_logger = logging.getLogger(__name__)


@requires_dev_features
def test_jobs(cfg: osparc.Configuration):
    """Test the jobs method

    Args:
        configuration (osparc.Configuration): The Configuration
    """
    solver: str = "simcore/services/comp/itis/sleeper"
    version: str = "2.0.2"
    n_jobs: int = 3
    with osparc.ApiClient(cfg) as api_client:
        solvers_api: osparc.SolversApi = osparc.SolversApi(api_client)
        sleeper: osparc.Solver = solvers_api.get_solver_release(solver, version)

        # initial iterator
        init_iter = solvers_api.jobs(sleeper.id, sleeper.version)
        n_init_iter: int = len(init_iter)
        assert n_init_iter >= 0

        # create n_jobs jobs
        created_job_ids = []
        for _ in range(n_jobs):
            job: osparc.Job = solvers_api.create_job(
                sleeper.id, sleeper.version, osparc.JobInputs({"input1": 1.0})
            )
            created_job_ids.append(job.id)

        tmp_iter = solvers_api.jobs(sleeper.id, sleeper.version)
        solvers_api.jobs(sleeper.id, sleeper.version)

        final_iter = solvers_api.jobs(sleeper.id, sleeper.version)
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


@requires_dev_features
async def test_logstreaming(cfg: osparc.Configuration):
    """Test the log streaming

    Args:
        configuration (osparc.Configuration): The Configuration
    """
    solver: str = "simcore/services/comp/itis/sleeper"
    version: str = "2.0.2"
    with osparc.ApiClient(cfg) as api_client:
        solvers_api: osparc.SolversApi = osparc.SolversApi(api_client)
        sleeper: osparc.Solver = solvers_api.get_solver_release(
            solver, version
        )  # type: ignore

        job: osparc.Job = solvers_api.create_job(
            sleeper.id, sleeper.version, osparc.JobInputs({"input1": 1.0})
        )  # type: ignore

        solvers_api.start_job(sleeper.id, sleeper.version, job.id)

        client = AsyncClient(
            base_url=cfg.host,
            auth=BasicAuth(username=cfg.username, password=cfg.password),
        )  # type: ignore
        nloglines: int = 0
        _logger.info("starting logstreaming...")
        async with client.stream(
            "GET",
            f"/v0/solvers/{sleeper.id}/releases/{sleeper.version}/jobs/{job.id}/logstream",
            timeout=15 * 60,
        ) as response:
            async for line in response.aiter_lines():
                nloglines += 1
                _logger.info(line)

        assert nloglines > 0, f"Could not stream log for {sleeper.id=}, \
            {sleeper.version=} and {job.id=}"  # type: ignore
        solvers_api.delete_job(sleeper.id, sleeper.version, job.id)
