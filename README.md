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
- Package version: 0.4.1
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
from __future__ import print_function
import time
import osparc
from osparc.rest import ApiException
from pprint import pprint

# Defining host is optional and default to https://api.osparc.io
configuration = osparc.Configuration()
configuration.host = "https://api.osparc.io"

# Enter a context with an instance of the API client
with osparc.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = osparc.MetaApi(api_client)

    try:
        # Get Service Metadata
        api_response = api_instance.get_service_metadata()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling MetaApi->get_service_metadata: %s\n" % e)

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
