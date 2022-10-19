![test](https://github.com/ITISFoundation/osparc-simcore-python-client/workflows/test/badge.svg)
[![PyPI](https://img.shields.io/pypi/v/osparc)](https://pypi.org/project/osparc/)
[![](https://img.shields.io/pypi/status/osparc)](https://pypi.org/project/osparc/)
[![](https://img.shields.io/pypi/l/osparc)](https://pypi.org/project/osparc/)


Python client for osparc-simcore public web API

- API version: 0.4.0
- Package version: 0.5.0

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

Please follow the installation procedure above, create an API key and secret in *https:/osparc.io*, add them as environment variables ``MY_API_KEY``, ``MY_API_SECRET`` and then run the following:

```python
import os
import time

import osparc
from osparc.models import File, Solver, Job, JobStatus, JobInputs, JobOutputs
from osparc.api import FilesApi, SolversApi

cfg = osparc.Configuration(
    username=os.environ.get("MY_API_KEY"),
    password=os.environ.get("MY_API_SECRET"),
)

with osparc.ApiClient(cfg) as api_client:
    users_api = osparc.UsersApi(api_client)
    print(users_api.get_my_profile())

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


## Documentation for API Classes

All URIs are relative to *https://api.osparc.io*

- [MetaApi](md/MetaApi.md)
- [FilesApi](md/FilesApi.md)
- [SolversApi](md/SolversApi.md)
- [UsersApi](md/UsersApi.md)


## Documentation For Models

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
