# Python client for osparc-simcore API

![test](https://github.com/ITISFoundation/osparc-simcore-python-client/workflows/test/badge.svg)
[![PyPI](https://img.shields.io/pypi/v/osparc)](https://pypi.org/project/osparc/)
[![](https://img.shields.io/pypi/status/osparc)](https://pypi.org/project/osparc/)
[![](https://img.shields.io/pypi/l/osparc)](https://pypi.org/project/osparc/)


<!--
TODO: activate when service is up and running in production
[![codecov](https://codecov.io/gh/ITISFoundation/osparc-simcore-python-client/branch/master/graph/badge.svg)](https://codecov.io/gh/ITISFoundation/osparc-simcore-python-client) -->


Python client for osparc-simcore public web API

- API version: 0.4.0
- Package version: 0.5.0
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

## Documentation for API Classes

All URIs are relative to *https://api.osparc.io*

- [MetaApi](docs/md/MetaApi.md)
- [FilesApi](docs/md/FilesApi.md)
- [SolversApi](docs/md/SolversApi.md)
- [UsersApi](docs/md/UsersApi.md)


## Documentation For Models

 - [File](docs/md/File.md)
 - [Groups](docs/md/Groups.md)
 - [HTTPValidationError](docs/md/HTTPValidationError.md)
 - [Job](docs/md/Job.md)
 - [JobInputs](docs/md/JobInputs.md)
 - [JobOutputs](docs/md/JobOutputs.md)
 - [JobStatus](docs/md/JobStatus.md)
 - [Meta](docs/md/Meta.md)
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
