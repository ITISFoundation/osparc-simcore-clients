# Basic Tutorial



## Installation
Install the python client and check the installation as follows:

```command
$ pip install osparc
$ python -c "import osparc; print(osparc.info.get_api())"
```


## Setup

To setup the client, we need to provide a username and password to the configuration. These can be obtained in the UI under [Preferences > API Settings > API Keys](http://docs.osparc.io/#/docs/platform_introduction/main_window_and_navigation/user_setup/profile?id=preferences). Use the *API key* as username and the *API secret* as password. For security reasons, you should not write these values in your script but instead set them up via environment variables or read them from a separate file. In this example, we use environment variables which will be referred to as "OSPARC_API_KEY" and "OSPARC_API_SECRET" for the rest of the tutorial.

```python

import os
from osparc import osparc_client

cfg = osparc_client.Configuration(
    username=os.environ["OSPARC_API_KEY"],
    password=os.environ["OSPARC_API_SECRET"],
)
print(cfg.host)

```

The configuration can now be used to create an instance of the API client. The API client is responsible of the communication with the osparc platform


The functions in the [osparc API] are grouped into sections such as *meta*, *users*, *files* or *solvers*. Each section address a different resource of the platform.


For example, the *users* section includes functions about the user (i.e. you) and can be accessed initializing a ``UsersApi``:

```python
from osparc import osparc_client
from osparc_client.api import UsersApi

with osparc_client.ApiClient(cfg) as api_client:

    users_api = UsersApi(api_client)

    profile = users_api.get_my_profile()
    print(profile)

    #
    #  {'first_name': 'foo',
    #  'gravatar_id': 'aa33fssec77ea434c2ea4fb92d0fd379e',
    #  'groups': {'all': {'description': 'all users',
    #                     'gid': '1',
    #                     'label': 'Everyone'},
    #             'me': {'description': 'primary group',
    #                    'gid': '2',
    #                    'label': 'foo'},
    #             'organizations': []},
    #  'last_name': '',
    #  'login': 'foo@itis.swiss',
    #  'role': 'USER'}
    #
```


## Solvers Workflow

The osparc API can be used to execute any computational service published in the platform. This means that any computational service listed in the UI under the [Discover Tab](http://docs.osparc.io/#/docs/platform_introduction/core_elements/Discover?id=discover-tab) is accessible from the API. Note that computational services are denoted as *solvers* in the API for convenience, but they refer to the same concept.


Let's use the sleepers computational service to illustrate a typical workflow. The sleepers computational service is a very basic service that simply waits (i.e. *sleeps*) a given time before producing some outputs. It takes as input one natural number, an optional text file input that contains another natural number and a boolean in the form of a checkbox. It also provides two outputs: one natural number and a file containing a single natural number.


```python
import time
from pathlib import Path
from zipfile import ZipFile

from osparc import osparc_client
from osparc_client.api import FilesApi, SolversApi
from osparc_client.models import File, Job, JobInputs, JobOutputs, JobStatus, Solver

CLIENT_VERSION = tuple(map(int, osparc_client.__version__.split(".")))
assert CLIENT_VERSION >= (0, 4, 3)

Path("file_with_number.txt").write_text("3")

with osparc_client.ApiClient(cfg) as api_client:

    files_api = FilesApi(api_client)
    input_file: File = files_api.upload_file(file="file_with_number.txt")

    solvers_api = SolversApi(api_client)
    solver: Solver = solvers_api.get_solver_release(
        "simcore/services/comp/itis/sleeper", "2.0.2"
    )

    job: Job = solvers_api.create_job(
        solver.id,
        solver.version,
        JobInputs(
            {
                "input_3": 0,
                "input_2": 3.0,
                "input_1": input_file,
            }
        ),
    )

    status: JobStatus = solvers_api.start_job(solver.id, solver.version, job.id)
    while not status.stopped_at:
        time.sleep(3)
        status = solvers_api.inspect_job(solver.id, solver.version, job.id)
        print("Solver progress", f"{status.progress}/100", flush=True)
    #
    # Solver progress 0/100
    # Solver progress 100/100

    outputs: JobOutputs = solvers_api.get_job_outputs(solver.id, solver.version, job.id)

    print(f"Job {outputs.job_id} got these results:")
    for output_name, result in outputs.results.items():
        print(output_name, "=", result)

    #
    # Job 19fc28f7-46fb-4e96-9129-5e924801f088 got these results:
    #
    # output_1 = {'checksum': '859fda0cb82fc4acb4686510a172d9a9-1',
    # 'content_type': 'text/plain',
    # 'filename': 'single_number.txt',
    # 'id': '9fb4f70e-3589-3e9e-991e-3059086c3aae'}
    # output_2 = 4.0

    if CLIENT_VERSION >= (0, 5, 0):
        logfile_path: str = solvers_api.get_job_output_logfile(
            solver.id, solver.version, job.id
        )
        zip_path = Path(logfile_path)

        extract_dir = Path("./extracted")
        extract_dir.mkdir()

        with ZipFile(f"{zip_path}") as fzip:
            fzip.extractall(f"{extract_dir}")

        logfiles = list(extract_dir.glob("*.log*"))
        print("Unzipped", logfiles[0], "contains:\n", logfiles[0].read_text())
    #
    # Unzipped extracted/sleeper_2.0.2.logs contains:
    # 2022-06-01T18:15:00.405035847+02:00 Entrypoint for stage production ...
    # 2022-06-01T18:15:00.421279969+02:00 User : uid=0(root) gid=0(root) groups=0(root)
    # 2022-06-01T18:15:00.421560331+02:00 Workdir : /home/scu
    # ...
    # 2022-06-01T18:15:00.864550043+02:00
    # 2022-06-01T18:15:03.923876794+02:00 Will sleep for 3 seconds
    # 2022-06-01T18:15:03.924473521+02:00 [PROGRESS] 1/3...
    # 2022-06-01T18:15:03.925021846+02:00 Remaining sleep time 0.9999995231628418
    # 2022-06-01T18:15:03.925558026+02:00 [PROGRESS] 2/3...
    # 2022-06-01T18:15:03.926103062+02:00 Remaining sleep time 0.9999985694885254
    # 2022-06-01T18:15:03.926643184+02:00 [PROGRESS] 3/3...
    # 2022-06-01T18:15:03.933544384+02:00 Remaining sleep time 0.9999983310699463

    download_path: str = files_api.download_file(file_id=outputs.results["output_1"].id)
    print(Path(download_path).read_text())
    #
    # 7

```

The script above

1. Uploads a file ``file_with_number.txt``
2. Selects version ``2.0.2`` of the ``sleeper``
3. Runs the ``sleeper`` and provides a reference to the uploaded file and other values as input parameters
4. Monitors the status of the solver while it is running in the platform
5. When the execution completes, it checks the outputs
6. The logs are downloaded, unzipped and saved to a new ```extracted``` directory
7. One of the outputs is a file and it is downloaded


#### Files

Files used as input to solvers or produced by solvers in the platform are accessible in the **files** section and specifically with the ``FilesApi`` class.
In order to use a file as input, it has to be uploaded first and the reference used in the corresponding solver's input.


```python
files_api = FilesApi(api_client)
input_file: File = files_api.upload_file(file="file_with_number.txt")


# ...


outputs: JobOutputs = solvers_api.get_job_outputs(solver.id, solver.version, job.id)
results_file: File = outputs.results["output_1"]
download_path: str = files_api.download_file(file_id=results_file.id)

```

In the snippet above, ``input_file`` is a ``File`` reference to the uploaded file and that is passed as input to the solver. Analogously, ``results_file`` is a ``File`` produced by the solver and that can also be downloaded.


#### Solvers, Inputs and Outputs

The inputs and outputs are specific for every solver. Every input/output has a name and an associated type that can be as simple as booleans, numbers, strings ... or more complex as files. You can find this information in the UI under Discover Tab, selecting the service card > More Info > raw metadata. For instance, the ``sleeper`` version ``2.0.2`` has the following ``raw-metadata``:

```json
{
    inputs: {
        'input_1': {'description': 'Pick a file containing only one '
                                    'integer',
                    'displayOrder': 1,
                    'fileToKeyMap': {'single_number.txt': 'input_1'},
                    'label': 'File with int number',
                    'type': 'data:text/plain'},
        'input_2': {'defaultValue': 2,
                    'description': 'Choose an amount of time to sleep',
                    'displayOrder': 2,
                    'label': 'Sleep interval',
                    'type': 'integer',
                    'unit': 'second'},
        'input_3': {'defaultValue': False,
                    'description': 'If set to true will cause service to '
                                    'fail after it sleeps',
                    'displayOrder': 3,
                    'label': 'Fail after sleep',
                    'type': 'boolean'},
    }
}
```
So, the inputs can be set as follows

```python
# ...
job = solvers_api.create_job(
            solver.id,
            solver.version,
            job_inputs=JobInputs(
                {
                    "input_1": uploaded_input_file,
                    "input_2": 3 * n,  # sleep time in secs
                    "input_3": bool(n % 2),  # fail after sleep?
                }
            ),
        )

```

And the metadata for the outputs are
```json
{
    'outputs': {'output_1': {'description': 'Integer is generated in range [1-9]',
                            'displayOrder': 1,
                            'fileToKeyMap': {'single_number.txt': 'output_1'},
                            'label': 'File containing one random integer',
                            'type': 'data:text/plain'},
                'output_2': {'description': 'Interval is generated in range '
                                            '[1-9]',
                            'displayOrder': 2,
                            'label': 'Random sleep interval',
                            'type': 'integer',
                            'unit': 'second'}},
}
```
so this information determines which output corresponds to a number or a file in the following snippet

```python
# ...

outputs: JobOutputs = solvers_api.get_job_outputs(solver.id, solver.version, job.id)

output_file = outputs.results["output_1"]
number = outputs.results["output_2"]

assert status.state == "SUCCESS"


assert isinstance(output_file, File)
assert isinstance(number, float)

# output file exists
assert files_api.get_file(output_file.id) == output_file

# can download and open
download_path: str = files_api.download_file(file_id=output_file.id)
assert float(Path(download_path).read_text()), "contains a random number"
```

#### Job Status

Once the client script triggers the solver, the solver runs in the platform and the script is freed. Sometimes, it is convenient to monitor the status of the run to see e.g. the progress of the execution or if the run was completed.

A solver runs in a plaforma starts a ``Job``. Using the ``solvers_api``, allows us to inspect the ``Job`` and get a ``JobStatus`` with information about its status. For instance

```python
 status: JobStatus = solvers_api.start_job(solver.id, solver.version, job.id)
 while not status.stopped_at:
     time.sleep(3)
     status = solvers_api.inspect_job(solver.id, solver.version, job.id)
     print("Solver progress", f"{status.progress}/100", flush=True)
```

#### Logs

When a solver runs, it will generate logs during execution which are then saved as .log files. Starting from the osparc Python Client version 0.5.0, The ``solvers_api`` also allows us to obtain the ``logfile_path`` associated with a particular ``Job``. This is a zip file that can then be extracted and saved. For instance

```python
logfile_path: str = solvers_api.get_job_output_logfile(
    solver.id, solver.version, job.id
)
zip_path = Path(logfile_path)

extract_dir = Path("./extracted")
extract_dir.mkdir()

with ZipFile(f"{zip_path}") as fzip:
    fzip.extractall(f"{extract_dir}")
```

## References

- [osparc API python client] documentation
- [osparc API] documentation
- A full script with this tutorial: [``sleeper.py``](https://github.com/ITISFoundation/osparc-simcore/blob/master/tests/public-api/examples/sleeper.py)

[osparc API python client]:https://itisfoundation.github.io/osparc-simcore-clients
[osparc API]:https://api.osparc.io/doc
[Download as BasicTutorial.ipynb](clients/python/docs/BasicTutorial.ipynb ":ignore title")
