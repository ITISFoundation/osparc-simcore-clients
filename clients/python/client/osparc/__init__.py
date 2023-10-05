"""
0.6.0 osparc client
"""
from typing import Tuple

import nest_asyncio
from osparc_client import (  # APIs; API client; models
    ApiClient,
    ApiException,
    ApiKeyError,
    ApiTypeError,
    ApiValueError,
    BodyUploadFileV0FilesContentPut,
    Configuration,
    ErrorGet,
    File,
    FilesApi,
    Groups,
    HTTPValidationError,
    Job,
    JobInputs,
    JobOutputs,
    JobStatus,
    Meta,
    MetaApi,
    OnePageSolverPort,
    OpenApiException,
    Profile,
    ProfileUpdate,
)
from osparc_client import RunningState as TaskStates
from osparc_client import (  # APIs; API client; models
    Solver,
    SolverPort,
    UserRoleEnum,
    UsersApi,
    UsersGroup,
    ValidationError,
    __version__,
)

from ._info import openapi
from ._solvers_api import SolversApi

nest_asyncio.apply()  # allow to run coroutines via asyncio.run(coro)

__all__: Tuple[str, ...] = (
    # imports from osparc_client
    "__version__",
    "FilesApi",
    "MetaApi",
    "SolversApi",
    "UsersApi",
    "BodyUploadFileV0FilesContentPut",
    "File",
    "Groups",
    "HTTPValidationError",
    "Job",
    "JobInputs",
    "JobOutputs",
    "JobStatus",
    "Meta",
    "Profile",
    "ProfileUpdate",
    "Solver",
    "TaskStates",
    "UserRoleEnum",
    "UsersGroup",
    "ValidationError",
    "ApiClient",
    "Configuration",
    "OpenApiException",
    "ApiTypeError",
    "ApiValueError",
    "ApiKeyError",
    "ApiException",
    "OnePageSolverPort",
    "SolverPort",
    "ErrorGet",
    # imports from osparc
    "openapi",
)
