#
# TODO: 'User-Agent': 'osparc-api/{packageVersion}/{language}'
#
#

import os
from pathlib import Path
from pprint import pformat, pprint
from typing import List

import osparc
import osparc.exceptions as errors
import packaging.version as pv
import pytest
from osparc.api.files_api import FilesApi
from osparc.configuration import Configuration
from osparc.models import FileUploaded, Meta, Solver, Job, JobState
from osparc.rest import ApiException


def as_dict(obj: object):
    return {
        attr: getattr(obj, attr)
        for attr in obj.__dict__.keys()
        if not attr.startswith("_")
    }




@pytest.fixture(scope="module")
def api_client(project_environ_patched):
    cfg = Configuration(
        host=os.environ.get("OSPARC_API_URL", "http://127.0.0.1:8000"),
        username=os.environ.get("OSPARC_API_KEY"),
        password=os.environ.get("OSPARC_API_SECRET"),
    )
    print("cfg", pformat(as_dict(cfg)))

    with osparc.ApiClient(cfg) as api_client:
        yield api_client


@pytest.fixture(scope="module")
def meta_api(api_client):
    return osparc.MetaApi(api_client)


@pytest.fixture(scope="module")
def files_api(api_client):
    return osparc.FilesApi(api_client)


@pytest.fixture(scope="module")
def solvers_api(api_client):
    return osparc.SolversApi(api_client)


# ----------

def test_get_service_metadata(meta_api):
    print("get Service Metadata", "-" * 10)
    meta: Meta = meta_api.get_service_metadata()
    print(meta)
    assert isinstance(meta, Meta)

    meta, status_code, headers = meta_api.get_service_metadata_with_http_info()

    assert isinstance(meta, Meta)
    assert status_code == 200


def test_upload_single_file(files_api):
    # some file
    input_path = Path("tmp-input.txt")
    input_path.write_text("demo")
    input_file: FileUploaded = files_api.upload_single_file(file=input_path)
    assert isinstance(input_file, FileUploaded)

    assert input_file.filename == input_path.name
    assert input_file.content_type == "text/plain"

    same_file = files_api.upload_single_file(file=input_path)
    assert input_file.hash == same_file.hash


def test_upload_list_download(files_api: FilesApi):
    input_path = Path("tmp-input.h5")
    input_path.write_bytes(b"demo")
    input_file: FileUploaded = files_api.upload_single_file(file=input_path)

    assert input_file.filename == input_path.name

    myfiles = files_api.list_files()
    assert myfiles
    assert input_file.to_dict() in myfiles

    same_file = files_api.download_file(file_id=input_file.hash)
    assert input_path.read_text() == same_file



def test_solvers(solvers_api):
    solvers: List[Solver] = solvers_api.list_solvers()
    
    latest = None
    for solver in solvers:
        if "isolve" in solver.name:
            if latest and pv.parse(latest.version) < pv.parse(solver.version):
                latest = solvers_api.get_solver_by_id(solver.uuid)

    print(latest)
    assert latest

    assert (
        solvers_api.get_solver_by_name_and_version(solver_name="isolve", version="latest")
        == latest
    )
    assert solvers_api.get_solver_by_id(latest.uuid) == latest

import datetime
import time


def test_run_solvers(solvers_api):
    solver = solvers_api.get_solver_by_name_and_version(solver_name="isolve", version="latest")
    assert isinstance(solver, Solver)

    #
    # Why creating a job and not just running directly from solver? 
    # Adding this intermediate step allows the server to do some extra checks before running a job.
    # For instance, does user has enough resources left? If not, the job could be rejected
    #

    # I would like to run a job with my solver and these inputs. 
    # TODO: how to name the body so we get nice doc?
    job = solvers_api.create_job(solver.uuid, job_input=[])

    # Job granted. Resources reserved for you during N-minutes
    assert isinstance(job, Job)

    # TODO: change to uid
    assert job.job_id
    assert job == solvers_api.get_job(job.job_id)

    # gets jobs granted for user with a given solver
    solver_jobs = solvers_api.list_jobs(solver.uuid)
    assert solver_jobs == [job, ]
    
    # I only have jobs from this solver ?
    all_jobs = solvers_api.list_all_jobs()
    assert all_jobs == solver_jobs


    # let's run the job
    submit_time = datetime.utcnow()
    state = solvers_api.start_job(job.job_id) 
    assert isinstance(state, JobState)

    assert state.status == "PENDING"
    assert state.progress == 0
    assert submit_time < state.submitted_at < submit_time + datetime.timedelta(seconds=1)


    while state.progress != 100:
        time.sleep(1)
        state = solvers_api.inspect_job(job.job_id)
        print("Solver progress", f"{state.progress}/100 completed")
    
    # done
    assert state.progress == 100
    assert state.status == ["SUCCESS", "FAILED"]
    assert state.submitted_at < state.started_at
    assert state.started_at < state.stopped_at

    # let's get the resouts


















