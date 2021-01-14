
#
# TODO: 'User-Agent': 'osparc-api/{packageVersion}/{language}'
#
#
from __future__ import print_function
import osparc.exceptions as errors
from pprint import pformat
import os
import time
from pathlib import Path
from pprint import pprint
from typing import List

import osparc
from osparc.configuration import Configuration
from osparc.models import FileUploaded, Meta, Solver
from osparc.rest import ApiException


def as_dict(obj: object):
    return { attr: getattr(obj, attr) for attr in obj.__dict__.keys() if not attr.startswith("_") }


def test_(solvers_api):
    print("get latests version LF solver", "-"*10)
    solvers: List[Solver] = solvers_api.list_solvers()
    my_solver = None
    for solver in solvers:
        if solver.name == "LF" and "latest" in solver.version_aliases:
            my_solver: Solver = solvers_api.get_solver_by_id(solver.uuid)
    print(my_solver)

    # shortcut
    assert (
        solvers.get_solver_by_name_and_version(solver_name="LF", version="latest")
        == my_solver
    )
    assert solvers.get_solver_by_id(my_solver.uuid) == my_solver



def test_get_service_metadata(meta_api):
    print("get Service Metadata", "-"*10)
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

    same_file= files_api.upload_single_file(file=input_path)
    assert input_file.hash == same_file.hash


def test_list_files(files_api):
    # Add files
    my_files: List[FileUploaded] = files_api.list_files()
    for f in my_files:
        assert isinstance(f, FileUploaded)

   

#######


cfg = Configuration(
    host=os.environ.get("OSPARC_API_URL", "http://127.0.0.1:8000"),
    username=os.environ.get("OSPARC_API_KEY"),
    password=os.environ.get("OSPARC_API_SECRET"),
)
print( "cfg", pformat(as_dict(cfg)))

with osparc.ApiClient(cfg) as api_client:
    meta_api = osparc.MetaApi(api_client)
    files_api = osparc.FilesApi(api_client)
    solvers_api = osparc.SolversApi(api_client)

    try:
        test_get_service_metadata(api_client)
        test_upload_single_file(files_api)



    except ApiException as err:
        print( "err: ", err, "\n", pformat(as_dict(err)))

    except errors.ApiTypeError as err:
        print( "err: ", err, "\n", pformat(as_dict(err)))

    except errors.ApiValueError as err:
        print( "err: ", err, "\n", pformat(as_dict(err)))

    except errors.ApiKeyError as err:
        print( "err: ", err, "\n", pformat(as_dict(err)))
