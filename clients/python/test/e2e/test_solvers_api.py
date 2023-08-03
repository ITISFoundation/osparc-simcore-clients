import os

import osparc
import pytest
from packaging.version import Version


@pytest.fixture
def configuration() -> osparc.Configuration:
    """Configuration

    Returns:
        osparc.Configuration: The Configuration
    """
    cfg = osparc.Configuration(
        host=os.environ["OSPARC_API_HOST"],
        username=os.environ["OSPARC_API_KEY"],
        password=os.environ["OSPARC_API_SECRET"],
    )
    return cfg


@pytest.mark.skipif(
    Version(osparc.__version__) < Version("0.6.0"),
    reason=f"osparc.__version__={osparc.__version__} is older than 0.6.0",
)
def test_get_jobs(configuration: osparc.Configuration):
    """Test the get_jobs method

    Args:
        configuration (osparc.Configuration): The Configuration
    """
    solver: str = "simcore/services/comp/itis/sleeper"
    version: str = "2.0.2"
    n_jobs: int = 3
    with osparc.ApiClient(configuration) as api_client:
        solvers_api: osparc.SolversApi = osparc.SolversApi(api_client)
        sleeper: osparc.Solver = solvers_api.get_solver_release(solver, version)

        # delete old jobs
        _, init_job_count = solvers_api.get_jobs(sleeper.id, sleeper.version, limit=3)

        # create n_jobs jobs
        created_job_ids = []
        for _ in range(n_jobs):
            job: osparc.Job = solvers_api.create_job(
                sleeper.id, sleeper.version, osparc.JobInputs({"input1": 1.0})
            )
            created_job_ids.append(job.id)

        job_iter, job_count = solvers_api.get_jobs(
            sleeper.id, sleeper.version, limit=3, offset=init_job_count
        )
        assert job_count > 0, "No jobs were available"
        assert (
            init_job_count + n_jobs == job_count
        ), "An incorrect number of jobs was recorded"

        for job in job_iter:
            assert isinstance(job, osparc.Job)

        # cleanup
        for elm in created_job_ids:
            solvers_api.delete_job(sleeper.id, sleeper.version, elm)
