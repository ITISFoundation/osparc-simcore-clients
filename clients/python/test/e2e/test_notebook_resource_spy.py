# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument

"""The spy the notebook tests prepend to every notebook they execute, and what it records.

The spy runs in a kernel the pytest process cannot reach, so nothing would notice if one of the
client methods it patched stopped existing or moved its arguments; what the notebooks create
would simply leak again. None of these tests needs a deployment.
"""

from pathlib import Path
from types import SimpleNamespace
from typing import Final

import _notebook_spy
import osparc
import pytest
from _utils import (
    RESOURCE_LOG_ENV_VAR,
    SOLVER_JOB,
    STUDY_JOB,
    UPLOADED_FILE,
    RecordedResource,
    delete_recorded_resources,
    read_recorded_resources,
)

_SOLVER_KEY: Final[str] = "simcore/services/dynamic/jupyter-smash"
_SOLVER_VERSION: Final[str] = "3.0.8"
_SOLVER_JOB_ID: Final[str] = "09e3bc39-6dd5-4c1e-b46e-e4cbe5a39d21"
_STUDY_ID: Final[str] = "bd5f1b8a-31f8-4b9d-a48d-3d3fe6a3f1c1"
_STUDY_JOB_ID: Final[str] = "5f8591e1-2bb9-4d0a-9c73-0d0ee81f9d2a"
_FILE_ID: Final[str] = "cc0b0b8a-7a1e-4b0b-9b9d-2c4d5e6f7a8b"


def _recorded(
    kind: str, key: str = "", version: str = "", resource_id: str = ""
) -> RecordedResource:
    return RecordedResource(
        kind=kind, key=key, version=version, resource_id=resource_id
    )


def test_spy_records_every_resource_a_notebook_creates(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # A path whose parent does not exist yet: the caller only picks the path, and nothing
    # guarantees the directory is there when the first resource shows up.
    resource_log = tmp_path / "artifacts" / "resources.jsonl"
    monkeypatch.setenv(RESOURCE_LOG_ENV_VAR, str(resource_log))
    monkeypatch.setattr(
        osparc.SolversApi,
        "create_job",
        lambda *args, **kwargs: SimpleNamespace(id=_SOLVER_JOB_ID),
    )
    monkeypatch.setattr(
        osparc.StudiesApi,
        "create_study_job",
        lambda *args, **kwargs: SimpleNamespace(id=_STUDY_JOB_ID),
    )
    monkeypatch.setattr(
        osparc.FilesApi,
        "upload_file",
        lambda *args, **kwargs: SimpleNamespace(id=_FILE_ID),
    )

    assert _notebook_spy.install() == (SOLVER_JOB, STUDY_JOB, UPLOADED_FILE)

    # Positional for the solver job, the way the notebooks in docs call it, and keyword for the
    # study job, which covers the other branch of the spy's lookup.
    osparc.SolversApi.create_job(None, _SOLVER_KEY, _SOLVER_VERSION, None)
    osparc.StudiesApi.create_study_job(None, study_id=_STUDY_ID, job_inputs=None)
    uploaded = osparc.FilesApi.upload_file(None, "file_with_number.txt")

    assert uploaded.id == _FILE_ID, "the spy hands the caller back what it wrapped"
    assert read_recorded_resources(resource_log) == [
        _recorded(SOLVER_JOB, _SOLVER_KEY, _SOLVER_VERSION, _SOLVER_JOB_ID),
        _recorded(STUDY_JOB, _STUDY_ID, "", _STUDY_JOB_ID),
        _recorded(UPLOADED_FILE, resource_id=_FILE_ID),
    ]


def test_spy_records_nothing_without_a_log(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # A notebook of a client version with fewer of these methods must still run, so the guards
    # have to keep the spy from failing when there is nowhere to record.
    monkeypatch.delenv(RESOURCE_LOG_ENV_VAR, raising=False)
    monkeypatch.setattr(
        osparc.SolversApi,
        "create_job",
        lambda *args, **kwargs: SimpleNamespace(id=_SOLVER_JOB_ID),
    )
    monkeypatch.setattr(
        osparc.FilesApi,
        "upload_file",
        lambda *args, **kwargs: SimpleNamespace(id=_FILE_ID),
    )

    _notebook_spy.install()

    assert osparc.SolversApi.create_job(None, _SOLVER_KEY, _SOLVER_VERSION, None)
    assert osparc.FilesApi.upload_file(None, "file_with_number.txt")


def test_recorded_files_are_deleted_after_the_jobs(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # A job input refers to the file it was uploaded from, so a file a job still uses cannot go
    # first. The log lists the file last here, the order that would break.
    deleted: list[str] = []
    monkeypatch.setattr(
        osparc.SolversApi, "stop_job", lambda *args: deleted.append(SOLVER_JOB)
    )
    monkeypatch.setattr(osparc.SolversApi, "delete_job", lambda *args: None)
    monkeypatch.setattr(
        osparc.FilesApi, "delete_file", lambda *args: deleted.append(UPLOADED_FILE)
    )

    configuration = osparc.Configuration(
        host="https://osparc.invalid", username="key", password="secret"
    )
    with osparc.ApiClient(configuration=configuration) as api_client:
        gone = delete_recorded_resources(
            api_client,
            [
                _recorded(UPLOADED_FILE, resource_id=_FILE_ID),
                _recorded(SOLVER_JOB, _SOLVER_KEY, _SOLVER_VERSION, _SOLVER_JOB_ID),
            ],
        )

    assert deleted == [SOLVER_JOB, UPLOADED_FILE]
    assert gone == 2
