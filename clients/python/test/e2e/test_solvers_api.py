import os

import osparc
import pytest


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
    osparc.__version__ < "0.6.0",
    reason=f"osparc.__version__={osparc.__version__} is older than 0.6.0",
)
def test_get_jobs(configuration: osparc.Configuration):
    """Test the get_jobs method

    Args:
        configuration (osparc.Configuration): The Configuration
    """
    solver: str = "simcore/services/comp/itis/sleeper"
    version: str = "2.0.2"
    n_jobs: int = 10
    with osparc.ApiClient(configuration) as api_client:
        solvers_api: osparc.SolversApi = osparc.SolversApi(api_client)
        sleeper: osparc.Solver = solvers_api.get_solver_release(solver, version)

        # delete old jobs
        for job in solvers_api.get_jobs(sleeper.id, sleeper.version, limit=3):
            solvers_api.delete_job(sleeper.id, sleeper.version, job.id)

        # create n_jobs jobs
        for _ in range(n_jobs):
            solvers_api.create_job(
                sleeper.id, sleeper.version, osparc.JobInputs({"input1": 1.0})
            )

        assert n_jobs == sum(
            1 for _ in solvers_api.get_jobs(sleeper.id, sleeper.version)
        )
