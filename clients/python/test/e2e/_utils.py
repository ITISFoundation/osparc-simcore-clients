import json
import logging
import subprocess
from collections.abc import Sequence
from pathlib import Path
from typing import Final, NamedTuple

import osparc
import pytest
import tenacity
from packaging.version import Version
from urllib3.exceptions import HTTPError as Urllib3HttpError

_logger = logging.getLogger(__name__)

# The notebook tests point this variable at a file, and hand it to the code they execute so
# that code can record the ids of the jobs it creates. See NOTEBOOK_JOB_SPY_CODE.
NOTEBOOK_JOB_LOG_ENV_VAR: Final[str] = "OSPARC_E2E_JOB_LOG"


class RecordedJob(NamedTuple):
    """A job a run created and needs deleting, as written to the job log.

    `key` is the solver key, or the study id when `kind` is `study`.
    """

    kind: str
    key: str
    version: str
    job_id: str


# Prepended to every notebook the tests execute, next to the HTTP logging cell. The notebooks
# submit jobs and have no teardown for them, and no fixture can reach an id created inside a
# cell, so the notebook reports them itself. Writing at creation time also means a notebook
# that fails mid-cell still leaves its ids behind for whoever cleans up after it.
#
# The notebook kernel is a separate process that cannot import this module, so the log variable
# is spelled out literally below and has to keep matching NOTEBOOK_JOB_LOG_ENV_VAR.
NOTEBOOK_JOB_SPY_CODE: Final[str] = """
import json as _json
import os as _os

import osparc as _osparc


def _e2e_record(job_kind, key, version, job):
    _log = _os.environ.get("OSPARC_E2E_JOB_LOG")
    if _log:
        # The caller picks the path, so it may not exist yet when the first job shows up.
        _dir = _os.path.dirname(_log)
        if _dir:
            _os.makedirs(_dir, exist_ok=True)
        with open(_log, "a") as _f:
            _f.write(
                _json.dumps(
                    {
                        "kind": job_kind,
                        "key": key,
                        "version": version,
                        "job_id": str(job.id),
                    }
                )
                + "\\n"
            )


# Guarded because the same spy runs against every client version in the matrix, and the oldest
# ones do not have all of these. The arguments are passed through untouched, and the two the log
# needs are read out of args/kwargs, so a client whose parameters are named differently than
# here cannot make the notebook it runs in fail. The first two arguments of create_job are the
# solver key and the version in every version in the matrix.
if getattr(_osparc, "SolversApi", None) is not None and hasattr(
    _osparc.SolversApi, "create_job"
):
    _create_solver_job = _osparc.SolversApi.create_job

    def _recorded_create_solver_job(self, *args, **kwargs):
        _job = _create_solver_job(self, *args, **kwargs)
        _e2e_record(
            "solver",
            args[0] if args else kwargs.get("solver_key"),
            args[1] if len(args) > 1 else kwargs.get("version"),
            _job,
        )
        return _job

    _osparc.SolversApi.create_job = _recorded_create_solver_job

if getattr(_osparc, "StudiesApi", None) is not None and hasattr(
    _osparc.StudiesApi, "create_study_job"
):
    _create_study_job = _osparc.StudiesApi.create_study_job

    def _recorded_create_study_job(self, *args, **kwargs):
        _job = _create_study_job(self, *args, **kwargs)
        _e2e_record(
            "study", args[0] if args else kwargs.get("study_id"), "", _job
        )
        return _job

    _osparc.StudiesApi.create_study_job = _recorded_create_study_job
"""


def read_recorded_jobs(path: Path) -> list[RecordedJob]:
    """The jobs a run recorded, oldest first. A missing file means none were recorded."""
    if not path.is_file():
        return []
    jobs: list[RecordedJob] = []
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        entry = json.loads(line)
        jobs.append(
            RecordedJob(
                kind=entry["kind"],
                key=entry["key"],
                version=entry.get("version", ""),
                job_id=entry["job_id"],
            )
        )
    return jobs


def _stop_and_delete(
    job: RecordedJob, solvers_api: osparc.SolversApi, studies_api: osparc.StudiesApi
) -> None:
    """Raises for any answer but 404, where the job is already gone."""
    try:
        if job.kind == "study":
            studies_api.stop_study_job(job.key, job.job_id)
            studies_api.delete_study_job(job.key, job.job_id)
        else:
            solvers_api.stop_job(job.key, job.version, job.job_id)
            solvers_api.delete_job(job.key, job.version, job.job_id)
    except osparc.ApiException as exc:
        if exc.status != 404:
            raise


def delete_recorded_jobs(
    api_client: osparc.ApiClient, jobs: Sequence[RecordedJob]
) -> int:
    """Stops and deletes the given jobs, retrying while the server settles.

    Returns how many of them the server no longer has afterwards, which covers both the job
    this call deleted and one that was already gone. A job that cannot be reached is logged and
    skipped, so one job cannot hide the rest.
    """
    solvers_api = osparc.SolversApi(api_client=api_client)
    studies_api = osparc.StudiesApi(api_client=api_client)
    absent = 0
    for job in jobs:
        try:
            for attempt in tenacity.Retrying(
                reraise=True,
                wait=tenacity.wait_fixed(2),
                stop=tenacity.stop_after_delay(60),
            ):
                with attempt:
                    _stop_and_delete(job, solvers_api, studies_api)
        except (osparc.ApiException, Urllib3HttpError) as exc:
            _logger.warning("Could not delete %s job %s: %s", job.kind, job.job_id, exc)
        else:
            absent += 1
    return absent


def sweep_all_jobs(api_client: osparc.ApiClient) -> int:
    """Deletes every job of every solver release this user owns.

    Only for a leak with no job log, since it also removes jobs a concurrent run is waiting
    on. Study jobs are not covered: the api-server exposes no way to list them.
    """
    solvers_api = osparc.SolversApi(api_client=api_client)
    deleted = 0
    releases = solvers_api.list_solvers_releases()
    _logger.info("Scanning %d solver releases", len(releases))
    for solver in releases:
        for job in solvers_api.iter_jobs(solver.id, solver.version):
            solvers_api.delete_job(solver.id, solver.version, job.id)
            deleted += 1
    return deleted


_clients_python_dir: Path = Path(__file__).parent.parent.parent
assert _clients_python_dir.is_dir()


def repo_version() -> Version:
    subprocess.run(
        "make VERSION", cwd=_clients_python_dir.resolve(), shell=True
    ).check_returncode()
    version_file: Path = Path(_clients_python_dir / "VERSION")
    assert version_file.is_file()
    return Version(version_file.read_text())


def skip_if_osparc_version(
    *,
    at_least: Version | None = None,
    at_most: Version | None = None,
    exactly: Version | None = None,
):
    def _wrapper(test):
        osparc_version = Version(osparc.__version__)
        if at_least and osparc_version < at_least:
            return pytest.mark.skip(f"{osparc_version=}<{at_least}")(test)
        if at_most and osparc_version > at_most:
            return pytest.mark.skip(f"{osparc_version=}>{at_most}")(test)
        if exactly and osparc_version != exactly:
            return pytest.mark.skip(f"{osparc_version=}!={exactly}")(test)
        return test

    return _wrapper
