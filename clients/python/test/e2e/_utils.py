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

# The notebook tests point this variable at a file and hand it to the code they execute, so that
# code can report what it created on the deployment. See NOTEBOOK_SPY_CODE.
RESOURCE_LOG_ENV_VAR: Final[str] = "OSPARC_E2E_RESOURCE_LOG"

# The kinds NOTEBOOK_SPY_CODE writes to that file. Deleting them needs different arguments, so
# they are distinguished rather than lumped together.
SOLVER_JOB: Final[str] = "solver"
STUDY_JOB: Final[str] = "study"
UPLOADED_FILE: Final[str] = "file"


class RecordedResource(NamedTuple):
    """What a run created on the deployment and needs deleting again.

    `key` is the solver key, or the study id of a study job. Both are empty for an uploaded
    file, which only needs its id.
    """

    kind: str
    key: str
    version: str
    resource_id: str


# Prepended to every notebook the tests execute, next to the HTTP logging cell. The notebooks
# upload a file and submit a job from it and have no teardown for either, and no fixture can
# reach an id created inside a cell, so the notebook reports them itself. Writing at creation
# time also means a notebook that fails mid-cell still leaves its ids behind for whoever cleans
# up after it.
#
# The notebook kernel is a separate process that cannot import this module, so the log variable
# is spelled out literally below and has to keep matching RESOURCE_LOG_ENV_VAR.
NOTEBOOK_SPY_CODE: Final[str] = """
import json as _json
import os as _os

import osparc as _osparc


def _e2e_record(kind, key, version, resource):
    _log = _os.environ.get("OSPARC_E2E_RESOURCE_LOG")
    if _log:
        # The caller picks the path, so it may not exist yet when the first resource shows up.
        _dir = _os.path.dirname(_log)
        if _dir:
            _os.makedirs(_dir, exist_ok=True)
        with open(_log, "a") as _f:
            _f.write(
                _json.dumps(
                    {
                        "kind": kind,
                        "key": key,
                        "version": version,
                        "resource_id": str(resource.id),
                    }
                )
                + "\\n"
            )


# Guarded because the same spy runs against every client version in the matrix, and the oldest
# ones do not have all of these. The arguments are passed through untouched, and the ones the
# log needs are read out of args/kwargs, so a client whose parameters are named differently
# than here cannot make the notebook it runs in fail. The first two arguments of create_job are
# the solver key and the version in every version in the matrix.
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
        _e2e_record("study", args[0] if args else kwargs.get("study_id"), "", _job)
        return _job

    _osparc.StudiesApi.create_study_job = _recorded_create_study_job

if getattr(_osparc, "FilesApi", None) is not None and hasattr(
    _osparc.FilesApi, "upload_file"
):
    _upload_file = _osparc.FilesApi.upload_file

    def _recorded_upload_file(self, *args, **kwargs):
        _file = _upload_file(self, *args, **kwargs)
        _e2e_record("file", "", "", _file)
        return _file

    _osparc.FilesApi.upload_file = _recorded_upload_file
"""


def read_recorded_resources(path: Path) -> list[RecordedResource]:
    """What a run recorded, oldest first. A missing file means nothing was recorded."""
    if not path.is_file():
        return []
    resources: list[RecordedResource] = []
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        entry = json.loads(line)
        resources.append(
            RecordedResource(
                kind=entry["kind"],
                key=entry["key"],
                version=entry.get("version", ""),
                resource_id=entry["resource_id"],
            )
        )
    return resources


def _delete(
    resource: RecordedResource,
    solvers_api: osparc.SolversApi,
    studies_api: osparc.StudiesApi,
    files_api: osparc.FilesApi,
) -> None:
    """Raises for any answer but 404, where the server already has nothing left to delete."""
    try:
        if resource.kind == STUDY_JOB:
            studies_api.stop_study_job(resource.key, resource.resource_id)
            studies_api.delete_study_job(resource.key, resource.resource_id)
        elif resource.kind == SOLVER_JOB:
            solvers_api.stop_job(resource.key, resource.version, resource.resource_id)
            solvers_api.delete_job(resource.key, resource.version, resource.resource_id)
        else:
            files_api.delete_file(resource.resource_id)
    except osparc.ApiException as exc:
        if exc.status != 404:
            raise


def delete_recorded_resources(
    api_client: osparc.ApiClient, resources: Sequence[RecordedResource]
) -> int:
    """Deletes what a run recorded, retrying while the server settles.

    Returns how many of them the server no longer has afterwards, which covers both the resource
    this call deleted and one that was already gone. A resource that cannot be reached is logged
    and skipped, so one of them cannot hide the rest.

    The jobs go before the files: a job input refers to the file it was uploaded from, and the
    server keeps a file a job still uses.
    """
    solvers_api = osparc.SolversApi(api_client=api_client)
    studies_api = osparc.StudiesApi(api_client=api_client)
    files_api = osparc.FilesApi(api_client=api_client)
    files_are_deletable = hasattr(files_api, "delete_file")
    absent = 0
    for resource in sorted(resources, key=lambda item: item.kind == UPLOADED_FILE):
        if resource.kind == UPLOADED_FILE and not files_are_deletable:
            _logger.warning(
                "Keeping file %s: this client version has no delete_file",
                resource.resource_id,
            )
            continue
        try:
            for attempt in tenacity.Retrying(
                reraise=True,
                wait=tenacity.wait_fixed(2),
                stop=tenacity.stop_after_delay(60),
            ):
                with attempt:
                    _delete(resource, solvers_api, studies_api, files_api)
        except (osparc.ApiException, Urllib3HttpError) as exc:
            _logger.warning(
                "Could not delete %s %s: %s", resource.kind, resource.resource_id, exc
            )
        else:
            absent += 1
    return absent


def sweep_all_jobs(api_client: osparc.ApiClient) -> int:
    """Deletes every job of every solver release this user owns.

    Only for a leak with no resource log, since it also removes jobs a concurrent run is waiting
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
