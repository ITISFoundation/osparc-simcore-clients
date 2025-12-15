# pylint: disable=protected-access
# pylint: disable=redefined-outer-name
# pylint: disable=too-many-arguments
# pylint: disable=unused-argument
# pylint: disable=unused-variable

import shutil
from datetime import timedelta
from pathlib import Path
from uuid import UUID

import osparc
import pytest
import tenacity
from _utils import skip_if_osparc_version
from packaging.version import Version

_WAIT_TIMEOUT = timedelta(minutes=15)


@skip_if_osparc_version(at_least=Version("0.6.6.post7"))
@pytest.mark.parametrize("download_dir", [True, False])
async def test_studies_logs(
    api_client: osparc.ApiClient,
    file_with_number: osparc.File,
    sleeper_study_id: UUID,
    download_dir: bool,
    tmp_path: Path,
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
    print(job)
    status = studies_api.start_study_job(study_id=f"{sleeper_study_id}", job_id=job.id)
    assert isinstance(status, osparc.JobStatus)
    async for attempt in tenacity.AsyncRetrying(
        reraise=True,
        wait=tenacity.wait_fixed(timedelta(seconds=5)),
        stop=tenacity.stop_after_delay(_WAIT_TIMEOUT),
        retry=tenacity.retry_if_exception_type(AssertionError),
    ):
        with attempt:
            status = studies_api.inspect_study_job(
                study_id=f"{sleeper_study_id}", job_id=job.id
            )
            assert isinstance(status, osparc.JobStatus)
            print(f"--- seconds idle: {attempt.retry_state.idle_for}\n", status)
            assert status.stopped_at is not None
    assert status.state == "SUCCESS"
    try:
        log_dir = await studies_api.get_study_job_output_logfiles_async(
            study_id=f"{sleeper_study_id}",
            job_id=job.id,
            download_dir=tmp_path if download_dir else None,
        )
        assert log_dir.is_dir()
        n_logfiles = sum(1 for _ in log_dir.rglob("*") if _.is_file())
        assert n_logfiles > 0
    finally:
        shutil.rmtree(log_dir)
