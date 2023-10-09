import osparc
from _utils import requires_dev_features


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
