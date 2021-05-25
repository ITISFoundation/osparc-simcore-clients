
![test](https://github.com/ITISFoundation/osparc-simcore-python-client/workflows/test/badge.svg)
[![PyPI](https://img.shields.io/pypi/v/osparc)](https://pypi.org/project/osparc/)
[![](https://img.shields.io/pypi/status/osparc)](https://pypi.org/project/osparc/)
[![](https://img.shields.io/pypi/l/osparc)](https://pypi.org/project/osparc/)


Python client for osparc-simcore public web API

- API version: 0.3.0
- Package version: 0.4.3
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

## Tutorials

- [Basic tutorial](md/tutorials/BasicTutorial.md)


## Documentation for API Endpoints

All URIs are relative to *https://api.osparc.io*

Class        | Method                                                                | HTTP request                                                               | Description
-------------|-----------------------------------------------------------------------|----------------------------------------------------------------------------|-------------------------------
*FilesApi*   | [**download_file**](md/FilesApi.md#download_file)                   | **GET** /v0/files/{file_id}/content                                        | Download File
*FilesApi*   | [**get_file**](md/FilesApi.md#get_file)                             | **GET** /v0/files/{file_id}                                                | Get File
*FilesApi*   | [**list_files**](md/FilesApi.md#list_files)                         | **GET** /v0/files                                                          | List Files
*FilesApi*   | [**upload_file**](md/FilesApi.md#upload_file)                       | **PUT** /v0/files/content                                                  | Upload File
*MetaApi*    | [**get_service_metadata**](md/MetaApi.md#get_service_metadata)      | **GET** /v0/meta                                                           | Get Service Metadata
*SolversApi* | [**create_job**](md/SolversApi.md#create_job)                       | **POST** /v0/solvers/{solver_key}/releases/{version}/jobs                  | Create Job
*SolversApi* | [**get_job**](md/SolversApi.md#get_job)                             | **GET** /v0/solvers/{solver_key}/releases/{version}/jobs/{job_id}          | Get Job
*SolversApi* | [**get_job_outputs**](md/SolversApi.md#get_job_outputs)             | **GET** /v0/solvers/{solver_key}/releases/{version}/jobs/{job_id}/outputs  | Get Job Outputs
*SolversApi* | [**get_solver**](md/SolversApi.md#get_solver)                       | **GET** /v0/solvers/{solver_key}/latest                                    | Get Latest Release of a Solver
*SolversApi* | [**get_solver_release**](md/SolversApi.md#get_solver_release)       | **GET** /v0/solvers/{solver_key}/releases/{version}                        | Get Solver Release
*SolversApi* | [**inspect_job**](md/SolversApi.md#inspect_job)                     | **POST** /v0/solvers/{solver_key}/releases/{version}/jobs/{job_id}:inspect | Inspect Job
*SolversApi* | [**list_jobs**](md/SolversApi.md#list_jobs)                         | **GET** /v0/solvers/{solver_key}/releases/{version}/jobs                   | List Jobs
*SolversApi* | [**list_solver_releases**](md/SolversApi.md#list_solver_releases)   | **GET** /v0/solvers/{solver_key}/releases                                  | List Solver Releases
*SolversApi* | [**list_solvers**](md/SolversApi.md#list_solvers)                   | **GET** /v0/solvers                                                        | List Solvers
*SolversApi* | [**list_solvers_releases**](md/SolversApi.md#list_solvers_releases) | **GET** /v0/solvers/releases                                               | Lists All Releases
*SolversApi* | [**start_job**](md/SolversApi.md#start_job)                         | **POST** /v0/solvers/{solver_key}/releases/{version}/jobs/{job_id}:start   | Start Job
*SolversApi* | [**stop_job**](md/SolversApi.md#stop_job)                           | **POST** /v0/solvers/{solver_key}/releases/{version}/jobs/{job_id}:stop    | Stop Job
*UsersApi*   | [**get_my_profile**](md/UsersApi.md#get_my_profile)                 | **GET** /v0/me                                                             | Get My Profile
*UsersApi*   | [**update_my_profile**](md/UsersApi.md#update_my_profile)           | **PUT** /v0/me                                                             | Update My Profile


## Documentation For Models

 - [BodyUploadFileV0FilesContentPut](md/BodyUploadFileV0FilesContentPut.md)
 - [File](md/File.md)
 - [Groups](md/Groups.md)
 - [HTTPValidationError](md/HTTPValidationError.md)
 - [Job](md/Job.md)
 - [JobInputs](md/JobInputs.md)
 - [JobOutputs](md/JobOutputs.md)
 - [JobStatus](md/JobStatus.md)
 - [Meta](md/Meta.md)
 - [Profile](md/Profile.md)
 - [ProfileUpdate](md/ProfileUpdate.md)
 - [Solver](md/Solver.md)
 - [TaskStates](md/TaskStates.md)
 - [UserRoleEnum](md/UserRoleEnum.md)
 - [UsersGroup](md/UsersGroup.md)
 - [ValidationError](md/ValidationError.md)


## Documentation For Authorization


## HTTPBasic

- **Type**: HTTP basic authentication


## Author

<p align="center">
<image src="_media/mwl.png" alt="made with love at z43" width="20%" />
</p>
