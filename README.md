# Python client for osparc-simcore API

![test](https://github.com/ITISFoundation/osparc-simcore-python-client/workflows/test/badge.svg)
[![PyPI](https://img.shields.io/pypi/v/osparc)](https://pypi.org/project/osparc/)
[![](https://img.shields.io/pypi/status/osparc)](https://pypi.org/project/osparc/)
[![](https://img.shields.io/pypi/l/osparc)](https://pypi.org/project/osparc/)


<!--
TODO: activate when service is up and running in production
[![codecov](https://codecov.io/gh/ITISFoundation/osparc-simcore-python-client/branch/master/graph/badge.svg)](https://codecov.io/gh/ITISFoundation/osparc-simcore-python-client) -->


Python client for osparc-simcore Public RESTful API

- API version: 0.4.0
- Package version: 0.4.0
- Build package: org.openapitools.codegen.languages.PythonClientCodegen

## Requirements

Python 3.6+

## Installation & Usage

Install the latest release with

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

# Defining host is optional and default to http://localhost
configuration = osparc.Configuration()
configuration.host = "https://localhost"

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

All URIs are relative to *http://localhost*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*FilesApi* | [**download_file**](docs/FilesApi.md#download_file) | **GET** /v0/files/{file_id}:download | Download File
*FilesApi* | [**files_upload_multiple_view**](docs/FilesApi.md#files_upload_multiple_view) | **GET** /v0/files/upload-multiple-view | Files Upload Multiple View
*FilesApi* | [**list_files**](docs/FilesApi.md#list_files) | **GET** /v0/files | List Files
*FilesApi* | [**upload_multiple_files**](docs/FilesApi.md#upload_multiple_files) | **POST** /v0/files:upload-multiple | Upload Multiple Files
*FilesApi* | [**upload_single_file**](docs/FilesApi.md#upload_single_file) | **POST** /v0/files:upload | Upload Single File
*MetaApi* | [**get_service_metadata**](docs/MetaApi.md#get_service_metadata) | **GET** /v0/meta | Get Service Metadata
*SolversApi* | [**create_job**](docs/SolversApi.md#create_job) | **POST** /v0/solvers/{solver_id}/jobs | Create Job
*SolversApi* | [**get_job**](docs/SolversApi.md#get_job) | **GET** /v0/solvers/{solver_id}/jobs/{job_id} | Get Job
*SolversApi* | [**get_job_output**](docs/SolversApi.md#get_job_output) | **GET** /v0/solvers/{solver_id}/jobs/{job_id}/outputs/{output_key} | Get Job Output
*SolversApi* | [**get_solver_by_id**](docs/SolversApi.md#get_solver_by_id) | **GET** /v0/solvers/{solver_id} | Get Solver By Id
*SolversApi* | [**get_solver_by_name_and_version**](docs/SolversApi.md#get_solver_by_name_and_version) | **GET** /v0/solvers/{solver_name}/{version} | Get Solver By Name And Version
*SolversApi* | [**inspect_job**](docs/SolversApi.md#inspect_job) | **POST** /v0/solvers/{solver_id}/jobs/{job_id}:inspect | Inspect Job
*SolversApi* | [**list_job_outputs**](docs/SolversApi.md#list_job_outputs) | **GET** /v0/solvers/{solver_id}/jobs/{job_id}/outputs | List Job Outputs
*SolversApi* | [**list_jobs**](docs/SolversApi.md#list_jobs) | **GET** /v0/solvers/{solver_id}/jobs | List Jobs
*SolversApi* | [**list_solvers**](docs/SolversApi.md#list_solvers) | **GET** /v0/solvers | List Solvers
*SolversApi* | [**run_job**](docs/SolversApi.md#run_job) | **POST** /v0/solvers/{solver_id}/jobs/{job_id}:run | Run Job
*SolversApi* | [**start_job**](docs/SolversApi.md#start_job) | **POST** /v0/solvers/{solver_id}/jobs/{job_id}:start | Start Job
*SolversApi* | [**stop_job**](docs/SolversApi.md#stop_job) | **POST** /v0/solvers/{solver_id}/jobs/{job_id}:stop | Stop Job
*UsersApi* | [**get_my_profile**](docs/UsersApi.md#get_my_profile) | **GET** /v0/me | Get My Profile
*UsersApi* | [**update_my_profile**](docs/UsersApi.md#update_my_profile) | **PUT** /v0/me | Update My Profile


## Documentation For Models

 - [BodyUploadMultipleFilesV0FilesUploadMultiplePost](docs/BodyUploadMultipleFilesV0FilesUploadMultiplePost.md)
 - [BodyUploadSingleFileV0FilesUploadPost](docs/BodyUploadSingleFileV0FilesUploadPost.md)
 - [FileUploaded](docs/FileUploaded.md)
 - [Groups](docs/Groups.md)
 - [HTTPValidationError](docs/HTTPValidationError.md)
 - [Job](docs/Job.md)
 - [JobInput](docs/JobInput.md)
 - [JobOutput](docs/JobOutput.md)
 - [JobState](docs/JobState.md)
 - [Meta](docs/Meta.md)
 - [Profile](docs/Profile.md)
 - [ProfileUpdate](docs/ProfileUpdate.md)
 - [Solver](docs/Solver.md)
 - [SolverOutput](docs/SolverOutput.md)
 - [TaskStates](docs/TaskStates.md)
 - [UserRoleEnum](docs/UserRoleEnum.md)
 - [UsersGroup](docs/UsersGroup.md)
 - [ValidationError](docs/ValidationError.md)


## Documentation For Authorization


## HTTPBasic

- **Type**: HTTP basic authentication


## Author

Made with love at [Zurich43](www.z43.swiss)
