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


def test_get_jobs_page(configuration: osparc.Configuration):
    """Test the get_jobs method

    Args:
        configuration (osparc.Configuration): The Configuration
    """
    solver: str = "simcore/services/comp/itis/sleeper"
    version: str = "2.0.2"
    with osparc.ApiClient(configuration) as api_client:
        solvers_api: osparc.SolversApi = osparc.SolversApi(api_client)
        sleeper: osparc.Solver = solvers_api.get_solver_release(solver, version)
