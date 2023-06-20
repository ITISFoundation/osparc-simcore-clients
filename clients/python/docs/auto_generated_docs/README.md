![test](https://github.com/ITISFoundation/osparc-simcore-clients/workflows/test/badge.svg)
[![PyPI](https://img.shields.io/pypi/v/osparc)](https://pypi.org/project/osparc/)
[![](https://img.shields.io/pypi/status/osparc)](https://pypi.org/project/osparc/)
[![](https://img.shields.io/pypi/l/osparc)](https://pypi.org/project/osparc/)

Python client for osparc-simcore public web API

- API version: 0.4.0
- Package version: 0.5.0

## Requirements.

Python 3.6+

## Installation & Usage
### pip install

To install run

```sh
pip install osparc
```
(you may need to run `pip` with root permission)

Then import the package:

```python
import osparc
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:

```python
import osparc
```

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:


```python
from __future__ import print_function
import time
import osparc
from osparc.rest import ApiException
from pprint import pprint

configuration = osparc.Configuration()
# Configure HTTP basic authorization: HTTPBasic
configuration.username = 'YOUR_API_KEY_HERE'
configuration.password = 'YOUR_API_SECRET_HERE'

# Enter a context with an instance of the API client
with osparc.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = osparc.FilesApi(api_client)
    file_id = 'file_id_example' # str |

    try:
        # Download File
        api_response = api_instance.download_file(file_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling FilesApi->download_file: %s\n" % e)

```

## Tutorials

- [Basic tutorial](../tutorials_and_samples/tutorials/BasicTutorial.md)

## Documentation for API Classes

All URIs are relative to *https://api.osparc.io*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*FilesApi* | [**download_file**](docs/FilesApi.md#download_file) | **GET** /v0/files/{file_id}/content | Download File
*FilesApi* | [**get_file**](docs/FilesApi.md#get_file) | **GET** /v0/files/{file_id} | Get File
*FilesApi* | [**list_files**](docs/FilesApi.md#list_files) | **GET** /v0/files | List Files
*FilesApi* | [**upload_file**](docs/FilesApi.md#upload_file) | **PUT** /v0/files/content | Upload File
*MetaApi* | [**get_service_metadata**](docs/MetaApi.md#get_service_metadata) | **GET** /v0/meta | Get Service Metadata
*SolversApi* | [**create_job**](docs/SolversApi.md#create_job) | **POST** /v0/solvers/{solver_key}/releases/{version}/jobs | Create Job
*SolversApi* | [**get_job**](docs/SolversApi.md#get_job) | **GET** /v0/solvers/{solver_key}/releases/{version}/jobs/{job_id} | Get Job
*SolversApi* | [**get_job_output_logfile**](docs/SolversApi.md#get_job_output_logfile) | **GET** /v0/solvers/{solver_key}/releases/{version}/jobs/{job_id}/outputs/logfile | Get Job Output Logfile
*SolversApi* | [**get_job_outputs**](docs/SolversApi.md#get_job_outputs) | **GET** /v0/solvers/{solver_key}/releases/{version}/jobs/{job_id}/outputs | Get Job Outputs
*SolversApi* | [**get_solver**](docs/SolversApi.md#get_solver) | **GET** /v0/solvers/{solver_key}/latest | Get Latest Release of a Solver
*SolversApi* | [**get_solver_release**](docs/SolversApi.md#get_solver_release) | **GET** /v0/solvers/{solver_key}/releases/{version} | Get Solver Release
*SolversApi* | [**inspect_job**](docs/SolversApi.md#inspect_job) | **POST** /v0/solvers/{solver_key}/releases/{version}/jobs/{job_id}:inspect | Inspect Job
*SolversApi* | [**list_jobs**](docs/SolversApi.md#list_jobs) | **GET** /v0/solvers/{solver_key}/releases/{version}/jobs | List Jobs
*SolversApi* | [**list_solver_releases**](docs/SolversApi.md#list_solver_releases) | **GET** /v0/solvers/{solver_key}/releases | List Solver Releases
*SolversApi* | [**list_solvers**](docs/SolversApi.md#list_solvers) | **GET** /v0/solvers | List Solvers
*SolversApi* | [**list_solvers_releases**](docs/SolversApi.md#list_solvers_releases) | **GET** /v0/solvers/releases | Lists All Releases
*SolversApi* | [**start_job**](docs/SolversApi.md#start_job) | **POST** /v0/solvers/{solver_key}/releases/{version}/jobs/{job_id}:start | Start Job
*SolversApi* | [**stop_job**](docs/SolversApi.md#stop_job) | **POST** /v0/solvers/{solver_key}/releases/{version}/jobs/{job_id}:stop | Stop Job
*UsersApi* | [**get_my_profile**](docs/UsersApi.md#get_my_profile) | **GET** /v0/me | Get My Profile
*UsersApi* | [**update_my_profile**](docs/UsersApi.md#update_my_profile) | **PUT** /v0/me | Update My Profile


## Documentation For Models

 - [BodyUploadFileV0FilesContentPut](docs/BodyUploadFileV0FilesContentPut.md)
 - [File](docs/File.md)
 - [Groups](docs/Groups.md)
 - [HTTPValidationError](docs/HTTPValidationError.md)
 - [Job](docs/Job.md)
 - [JobInputs](docs/JobInputs.md)
 - [JobOutputs](docs/JobOutputs.md)
 - [JobStatus](docs/JobStatus.md)
 - [Meta](docs/Meta.md)
 - [Profile](docs/Profile.md)
 - [ProfileUpdate](docs/ProfileUpdate.md)
 - [Solver](docs/Solver.md)
 - [TaskStates](docs/TaskStates.md)
 - [UserRoleEnum](docs/UserRoleEnum.md)
 - [UsersGroup](docs/UsersGroup.md)
 - [ValidationError](docs/ValidationError.md)


## Documentation For Authorization


## HTTPBasic

- **Type**: HTTP basic authentication


## Author

<p align="center">
<image src="../../../../docs/_media/mwl.png" alt="made with love at z43" width="20%" />
</p>
