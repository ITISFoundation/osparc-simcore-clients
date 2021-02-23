# Python client for osparc-simcore API

![test](https://github.com/ITISFoundation/osparc-simcore-python-client/workflows/test/badge.svg)
[![PyPI](https://img.shields.io/pypi/v/osparc)](https://pypi.org/project/osparc/)
[![](https://img.shields.io/pypi/status/osparc)](https://pypi.org/project/osparc/)
[![](https://img.shields.io/pypi/l/osparc)](https://pypi.org/project/osparc/)


<!--
TODO: activate when service is up and running in production
[![codecov](https://codecov.io/gh/ITISFoundation/osparc-simcore-python-client/branch/master/graph/badge.svg)](https://codecov.io/gh/ITISFoundation/osparc-simcore-python-client) -->


Python client for osparc-simcore public web API

- API version: 0.3.0
- Package version: 0.4.2
- Build package: org.openapitools.codegen.languages.PythonClientCodegen

## Requirements

Python 3.6+

## Installation & Usage

Install the [latest release](https://github.com/ITISFoundation/osparc-simcore-python-client/releases) with

```sh
pip install osparc
```
or directly from the repository
```sh
pip install git+https://github.com/ITISFoundation/osparc-simcore-python-client.git
```

Then import the package:

```python
import osparc
```

## Getting Started

Please follow the installation procedure above and then run the following:

```python
import os
import time

import osparc
from osparc.models import File, Solver, Job, JobStatus, JobInputs, JobOutputs
from osparc.api import FilesApi, SolversApi

cfg = osparc.Configuration(
    host=os.environ.get("OSPARC_API_URL", "http://127.0.0.1:8006"),
    username=os.environ.get("MY_API_KEY"),
    password=os.environ.get("MY_API_SECRET"),
)

with osparc.ApiClient(cfg) as api_client:

    files_api = FilesApi(api_client)
    input_file: File = files_api.upload_file(file="path/to/input-file.h5")


    solvers_api = SolversApi(api_client)
    solver: Solver = solvers_api.get_solver_release("simcore/services/comp/isolve", "1.2.3")

    job: Job = solvers_api.create_job(
        solver.id,
        solver.version,
        JobInputs({"input_1": input_file, "input_2": 33, "input_3": False}),
    )

    status: JobStatus = solvers_api.start_job(solver.id, solver.version, job.id)
    while not status.stopped_at:
        time.sleep(3)
        status = solvers_api.inspect_job(solver.id, solver.version, job.id)
        print("Solver progress", f"{status.progress}/100", flush=True)

    outputs: JobOutputs = solvers_api.get_job_outputs(solver.id, solver.version, job.id)

    print( f"Job {outputs.job_id} got these results:")
    for output_name, result in outputs.results.items():
        print(output_name, "=", result)

```


## Documentation for API Endpoints

All URIs are relative to *https://api.osparc.io*

Class        | Method                                                                                  | HTTP request                                    | Description
-------------|-----------------------------------------------------------------------------------------|-------------------------------------------------|-------------------------------
*FilesApi*   | [**download_file**](docs/md/FilesApi.md#download_file)                                     | **GET** /v0/files/{file_id}/content             | Download File
*FilesApi*   | [**get_file**](docs/md/FilesApi.md#get_file)                                               | **GET** /v0/files/{file_id}                     | Get File
*FilesApi*   | [**list_files**](docs/md/FilesApi.md#list_files)                                           | **GET** /v0/files                               | List Files
*FilesApi*   | [**upload_file**](docs/md/FilesApi.md#upload_file)                                         | **PUT** /v0/files/content                       | Upload File
*JobsApi*    | [**get_job**](docs/md/JobsApi.md#get_job)                                                  | **GET** /v0/jobs/{job_id}                       | Get Job
*JobsApi*    | [**get_job_output**](docs/md/JobsApi.md#get_job_output)                                    | **GET** /v0/jobs/{job_id}/outputs/{output_name} | Get Job Output
*JobsApi*    | [**inspect_job**](docs/md/JobsApi.md#inspect_job)                                          | **POST** /v0/jobs/{job_id}:inspect              | Inspect Job
*JobsApi*    | [**list_all_jobs**](docs/md/JobsApi.md#list_all_jobs)                                      | **GET** /v0/jobs                                | List All Jobs
*JobsApi*    | [**list_job_outputs**](docs/md/JobsApi.md#list_job_outputs)                                | **GET** /v0/jobs/{job_id}/outputs               | List Job Outputs
*JobsApi*    | [**start_job**](docs/md/JobsApi.md#start_job)                                              | **POST** /v0/jobs/{job_id}:start                | Start Job
*JobsApi*    | [**stop_job**](docs/md/JobsApi.md#stop_job)                                                | **POST** /v0/jobs/{job_id}:stop                 | Stop Job
*MetaApi*    | [**get_service_metadata**](docs/md/MetaApi.md#get_service_metadata)                        | **GET** /v0/meta                                | Get Service Metadata
*SolversApi* | [**create_job**](docs/md/SolversApi.md#create_job)                                         | **POST** /v0/solvers/{solver_id}/jobs           | Create Job
*SolversApi* | [**get_solver**](docs/md/SolversApi.md#get_solver)                                         | **GET** /v0/solvers/{solver_id}                 | Get Solver
*SolversApi* | [**get_solver_by_name_and_version**](docs/md/SolversApi.md#get_solver_by_name_and_version) | **GET** /v0/solvers/{solver_name}/{version}     | Get Solver By Name And Version
*SolversApi* | [**list_jobs**](docs/md/SolversApi.md#list_jobs)                                           | **GET** /v0/solvers/{solver_id}/jobs            | List Jobs
*SolversApi* | [**list_solvers**](docs/md/SolversApi.md#list_solvers)                                     | **GET** /v0/solvers                             | List Solvers
*UsersApi*   | [**get_my_profile**](docs/md/UsersApi.md#get_my_profile)                                   | **GET** /v0/me                                  | Get My Profile
*UsersApi*   | [**update_my_profile**](docs/md/UsersApi.md#update_my_profile)                             | **PUT** /v0/me                                  | Update My Profile


## Documentation For Models

 - [BodyUploadFileV0FilesContentPut](docs/md/BodyUploadFileV0FilesContentPut.md)
 - [FileMetadata](docs/md/FileMetadata.md)
 - [Groups](docs/md/Groups.md)
 - [HTTPValidationError](docs/md/HTTPValidationError.md)
 - [Job](docs/md/Job.md)
 - [JobInput](docs/md/JobInput.md)
 - [JobOutput](docs/md/JobOutput.md)
 - [JobStatus](docs/md/JobStatus.md)
 - [Meta](docs/md/Meta.md)
 - [PortValue](docs/md/PortValue.md)
 - [Profile](docs/md/Profile.md)
 - [ProfileUpdate](docs/md/ProfileUpdate.md)
 - [Solver](docs/md/Solver.md)
 - [TaskStates](docs/md/TaskStates.md)
 - [UserRoleEnum](docs/md/UserRoleEnum.md)
 - [UsersGroup](docs/md/UsersGroup.md)
 - [ValidationError](docs/md/ValidationError.md)

## Documentation For Authorization


## HTTPBasic

- **Type**: HTTP basic authentication


## Author

Made with love at [Zurich43](www.z43.swiss)
