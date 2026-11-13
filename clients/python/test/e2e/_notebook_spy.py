"""Records the resources the notebook tests create on the deployment.

The notebook tests prepend a cell calling install() to every notebook they execute, which makes
this the way the notebooks report what they created: they upload a file and submit a job from it
with no teardown of their own, and no fixture can reach an id created inside a cell. Recording
when the resource is created means a notebook that fails mid-cell still leaves its ids behind,
for the test's own teardown or for cleanup_resources.py.

The kernel is a separate process, but it runs the same interpreter with this directory added to
sys.path, so the contract constants come from _utils rather than being copied here.
"""

import json
import os
from pathlib import Path
from typing import Any, Final

import osparc
from _utils import RESOURCE_LOG_ENV_VAR, SOLVER_JOB, STUDY_JOB, UPLOADED_FILE

__all__: Final[list[str]] = ["install"]


def _record(kind: str, key: str, version: str, resource: Any) -> None:
    logged = os.environ.get(RESOURCE_LOG_ENV_VAR)
    if not logged:
        return
    # The caller picks the path, so the directory may not exist yet when the first resource
    # shows up.
    log_file = Path(logged)
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with log_file.open("a") as writer:
        writer.write(
            json.dumps(
                {
                    "kind": kind,
                    "key": key,
                    "version": version,
                    "resource_id": str(resource.id),
                }
            )
            + "\n"
        )


def install() -> tuple[str, ...]:
    """Patches the client so created resources get recorded, and returns what it patched.

    The guards are needed because the same spy runs against every client version in the matrix,
    and the oldest ones do not have all of these. The arguments are passed through untouched and
    the ones the log needs are read out of args/kwargs, so a client that names its parameters
    differently than here cannot make the notebook it runs in fail. The first two arguments of
    create_job are the solver key and the version in every version in the matrix.
    """
    patched: list[str] = []

    if getattr(osparc, "SolversApi", None) is not None and hasattr(
        osparc.SolversApi, "create_job"
    ):
        create_job = osparc.SolversApi.create_job

        def recorded_create_solver_job(self: Any, *args: Any, **kwargs: Any) -> Any:
            job = create_job(self, *args, **kwargs)
            _record(
                SOLVER_JOB,
                args[0] if args else kwargs.get("solver_key"),
                args[1] if len(args) > 1 else kwargs.get("version"),
                job,
            )
            return job

        osparc.SolversApi.create_job = recorded_create_solver_job  # type: ignore[method-assign]
        patched.append(SOLVER_JOB)

    if getattr(osparc, "StudiesApi", None) is not None and hasattr(
        osparc.StudiesApi, "create_study_job"
    ):
        create_study_job = osparc.StudiesApi.create_study_job

        def recorded_create_study_job(self: Any, *args: Any, **kwargs: Any) -> Any:
            job = create_study_job(self, *args, **kwargs)
            _record(STUDY_JOB, args[0] if args else kwargs.get("study_id"), "", job)
            return job

        osparc.StudiesApi.create_study_job = recorded_create_study_job  # type: ignore[method-assign]
        patched.append(STUDY_JOB)

    if getattr(osparc, "FilesApi", None) is not None and hasattr(
        osparc.FilesApi, "upload_file"
    ):
        upload_file = osparc.FilesApi.upload_file

        def recorded_upload_file(self: Any, *args: Any, **kwargs: Any) -> Any:
            uploaded = upload_file(self, *args, **kwargs)
            _record(UPLOADED_FILE, "", "", uploaded)
            return uploaded

        osparc.FilesApi.upload_file = recorded_upload_file  # type: ignore[method-assign]
        patched.append(UPLOADED_FILE)

    return tuple(patched)
