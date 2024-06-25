import shutil
from uuid import UUID

import osparc
import tenacity


async def test_studies_logs(
    api_client: osparc.ApiClient, file_with_number: osparc.File, sleeper_study_id: UUID
):
    studies_api = osparc.StudiesApi(api_client=api_client)
    job_inputs = osparc.JobInputs(
        values={
            "input_file": file_with_number,
        }
    )
    job = studies_api.create_study_job(
        study_id=f"{sleeper_study_id}", job_inputs=job_inputs
    )
    assert isinstance(job, osparc.Job)
    print(f"Running study job: {job.id}")
    status = studies_api.start_study_job(study_id=f"{sleeper_study_id}", job_id=job.id)
    assert isinstance(status, osparc.JobStatus)
    async for attempt in tenacity.AsyncRetrying(
        reraise=True,
        wait=tenacity.wait_fixed(1),
        stop=tenacity.stop_after_delay(30),
        retry=tenacity.retry_if_exception_type(AssertionError),
    ):
        with attempt:
            status = studies_api.inspect_study_job(
                study_id=f"{sleeper_study_id}", job_id=job.id
            )
            assert isinstance(status, osparc.JobStatus)
            assert status.stopped_at is not None
    assert status.state == "SUCCESS"
    try:
        log_dir = await studies_api.get_study_job_output_logfiles_async(
            study_id=f"{sleeper_study_id}", job_id=job.id
        )
        assert log_dir.is_dir()
        n_logfiles = sum(1 for _ in log_dir.rglob("*") if _.is_file())
        assert n_logfiles > 0
    finally:
        shutil.rmtree(log_dir)
