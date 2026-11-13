# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument

"""The spy the notebook tests inject into every notebook they execute.

It runs in a kernel the pytest process cannot reach, so nothing would notice if one of the
client methods it patches stopped existing or moved its arguments; the jobs the notebooks
create would simply leak again. This covers the patching and the log format, and it needs no
deployment to do so.
"""

from pathlib import Path
from types import SimpleNamespace

import osparc
import pytest
from _utils import (
    NOTEBOOK_JOB_LOG_ENV_VAR,
    NOTEBOOK_JOB_SPY_CODE,
    RecordedJob,
    read_recorded_jobs,
)

_SOLVER_KEY = "simcore/services/dynamic/jupyter-smash"
_SOLVER_VERSION = "3.0.8"
_SOLVER_JOB_ID = "09e3bc39-6dd5-4c1e-b46e-e4cbe5a39d21"
_STUDY_ID = "bd5f1b8a-31f8-4b9d-a48d-3d3fe6a3f1c1"
_STUDY_JOB_ID = "5f8591e1-2bb9-4d0a-9c73-0d0ee81f9d2a"


def test_notebook_job_spy_records_created_jobs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # A path whose parent does not exist yet, as the caller only picks the path and nothing
    # guarantees the directory.
    job_log = tmp_path / "artifacts" / "jobs.jsonl"
    monkeypatch.setenv(NOTEBOOK_JOB_LOG_ENV_VAR, str(job_log))

    create_job = osparc.SolversApi.create_job
    create_study_job = osparc.StudiesApi.create_study_job
    try:
        osparc.SolversApi.create_job = lambda *args, **kwargs: SimpleNamespace(
            id=_SOLVER_JOB_ID
        )
        osparc.StudiesApi.create_study_job = lambda *args, **kwargs: SimpleNamespace(
            id=_STUDY_JOB_ID
        )
        exec(NOTEBOOK_JOB_SPY_CODE, {})

        # Positional, the way the notebooks in docs call it, and by keyword for the other
        # branch of the spy's lookup.
        osparc.SolversApi.create_job(None, _SOLVER_KEY, _SOLVER_VERSION, None)
        osparc.StudiesApi.create_study_job(None, study_id=_STUDY_ID, job_inputs=None)
    finally:
        osparc.SolversApi.create_job = create_job
        osparc.StudiesApi.create_study_job = create_study_job

    assert read_recorded_jobs(job_log) == [
        RecordedJob(
            kind="solver",
            key=_SOLVER_KEY,
            version=_SOLVER_VERSION,
            job_id=_SOLVER_JOB_ID,
        ),
        RecordedJob(
            kind="study",
            key=_STUDY_ID,
            version="",
            job_id=_STUDY_JOB_ID,
        ),
    ]
