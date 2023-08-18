import asyncio

import osparc
import pytest
from packaging.version import Version


@pytest.mark.skipif(
    Version(osparc.__version__) < Version("0.6.0"),
    reason=f"osparc.__version__={osparc.__version__} is older than 0.6.0",
)
def test_get_jobs(cfg: osparc.Configuration):
    """Test the get_jobs method

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
        init_iter = solvers_api.get_jobs(sleeper.id, sleeper.version, limit=3)
        n_init_iter: int = len(init_iter)
        assert n_init_iter >= 0

        # create n_jobs jobs
        created_job_ids = []
        for _ in range(n_jobs):
            job: osparc.Job = solvers_api.create_job(
                sleeper.id, sleeper.version, osparc.JobInputs({"input1": 1.0})
            )
            created_job_ids.append(job.id)

        tmp_iter = solvers_api.get_jobs(
            sleeper.id, sleeper.version, limit=3, offset=n_init_iter
        )
        tmp_async_iter = solvers_api.get_jobs(
            sleeper.id, sleeper.version, limit=3, offset=n_init_iter
        )

        final_iter = solvers_api.get_jobs(sleeper.id, sleeper.version, limit=3)
        assert len(final_iter) > 0, "No jobs were available"
        assert n_init_iter + n_jobs == len(
            final_iter
        ), "An incorrect number of jobs was recorded"

        for elm in tmp_iter:
            assert isinstance(elm, osparc.Job)

        async def return_iter_content(
            i: osparc.PaginationGenerator,
        ) -> list[osparc.Job]:
            result = []
            async for elm in i:
                result.append(elm)
            return result

        for elm in asyncio.run(return_iter_content(tmp_async_iter)):
            assert isinstance(elm, osparc.Job)

        # cleanup
        for elm in created_job_ids:
            solvers_api.delete_job(sleeper.id, sleeper.version, elm)
