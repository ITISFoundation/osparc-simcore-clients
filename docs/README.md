# Current Version

![test](https://github.com/ITISFoundation/osparc-simcore-python-client/workflows/test/badge.svg)
[![PyPI](https://img.shields.io/pypi/v/osparc)](https://pypi.org/project/osparc/)
[![](https://img.shields.io/pypi/status/osparc)](https://pypi.org/project/osparc/)
[![](https://img.shields.io/pypi/l/osparc)](https://pypi.org/project/osparc/)


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

# Documentation for API Endpoints

All URIs are relative to *http://localhost*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*FilesApi* | [**download_file**](md/FilesApi.md#download_file) | **GET** /v0/files/{file_id}:download | Download File
*FilesApi* | [**files_upload_multiple_view**](md/FilesApi.md#files_upload_multiple_view) | **GET** /v0/files/upload-multiple-view | Files Upload Multiple View
*FilesApi* | [**list_files**](md/FilesApi.md#list_files) | **GET** /v0/files | List Files
*FilesApi* | [**upload_multiple_files**](md/FilesApi.md#upload_multiple_files) | **POST** /v0/files:upload-multiple | Upload Multiple Files
*FilesApi* | [**upload_single_file**](md/FilesApi.md#upload_single_file) | **POST** /v0/files:upload | Upload Single File
*MetaApi* | [**get_service_metadata**](md/MetaApi.md#get_service_metadata) | **GET** /v0/meta | Get Service Metadata
*SolversApi* | [**create_job**](md/SolversApi.md#create_job) | **POST** /v0/solvers/{solver_id}/jobs | Create Job
*SolversApi* | [**get_job**](md/SolversApi.md#get_job) | **GET** /v0/solvers/{solver_id}/jobs/{job_id} | Get Job
*SolversApi* | [**get_job_output**](md/SolversApi.md#get_job_output) | **GET** /v0/solvers/{solver_id}/jobs/{job_id}/outputs/{output_key} | Get Job Output
*SolversApi* | [**get_solver_by_id**](md/SolversApi.md#get_solver_by_id) | **GET** /v0/solvers/{solver_id} | Get Solver By Id
*SolversApi* | [**get_solver_by_name_and_version**](md/SolversApi.md#get_solver_by_name_and_version) | **GET** /v0/solvers/{solver_name}/{version} | Get Solver By Name And Version
*SolversApi* | [**inspect_job**](md/SolversApi.md#inspect_job) | **POST** /v0/solvers/{solver_id}/jobs/{job_id}:inspect | Inspect Job
*SolversApi* | [**list_job_outputs**](md/SolversApi.md#list_job_outputs) | **GET** /v0/solvers/{solver_id}/jobs/{job_id}/outputs | List Job Outputs
*SolversApi* | [**list_jobs**](md/SolversApi.md#list_jobs) | **GET** /v0/solvers/{solver_id}/jobs | List Jobs
*SolversApi* | [**list_solvers**](md/SolversApi.md#list_solvers) | **GET** /v0/solvers | List Solvers
*SolversApi* | [**run_job**](md/SolversApi.md#run_job) | **POST** /v0/solvers/{solver_id}/jobs/{job_id}:run | Run Job
*SolversApi* | [**start_job**](md/SolversApi.md#start_job) | **POST** /v0/solvers/{solver_id}/jobs/{job_id}:start | Start Job
*SolversApi* | [**stop_job**](md/SolversApi.md#stop_job) | **POST** /v0/solvers/{solver_id}/jobs/{job_id}:stop | Stop Job
*UsersApi* | [**get_my_profile**](md/UsersApi.md#get_my_profile) | **GET** /v0/me | Get My Profile
*UsersApi* | [**update_my_profile**](md/UsersApi.md#update_my_profile) | **PUT** /v0/me | Update My Profile


# Documentation For Models

 - [BodyUploadMultipleFilesV0FilesUploadMultiplePost](md/BodyUploadMultipleFilesV0FilesUploadMultiplePost.md)
 - [BodyUploadSingleFileV0FilesUploadPost](md/BodyUploadSingleFileV0FilesUploadPost.md)
 - [FileUploaded](md/FileUploaded.md)
 - [Groups](md/Groups.md)
 - [HTTPValidationError](md/HTTPValidationError.md)
 - [Job](md/Job.md)
 - [JobInput](md/JobInput.md)
 - [JobOutput](md/JobOutput.md)
 - [JobState](md/JobState.md)
 - [Meta](md/Meta.md)
 - [Profile](md/Profile.md)
 - [ProfileUpdate](md/ProfileUpdate.md)
 - [Solver](md/Solver.md)
 - [SolverOutput](md/SolverOutput.md)
 - [TaskStates](md/TaskStates.md)
 - [UserRoleEnum](md/UserRoleEnum.md)
 - [UsersGroup](md/UsersGroup.md)
 - [ValidationError](md/ValidationError.md)


# Documentation For Authorization


# HTTPBasic

- **Type**: HTTP basic authentication


# Author

<p align="center">
<image src="_media/mwl.png" alt="made with love at z43" width="20%" />
</p>
