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
    Groups,
    HTTPValidationError,
    Job,
    JobInputs,
    JobMetadata,
    JobMetadataUpdate,
    JobOutputs,
    JobStatus,
    Links,
    Meta,
    MetaApi,
    OnePageSolverPort,
    OnePageStudyPort,
    OpenApiException,
    Profile,
    ProfileUpdate,
)
from osparc_client import RunningState as TaskStates
from osparc_client import (  # APIs; API client; models
    Solver,
    SolverPort,
    StudiesApi,
    Study,
    StudyPort,
    UserRoleEnum,
    UsersApi,
    UsersGroup,
    ValidationError,
    __version__,
)

from ._files_api import FilesApi
from ._info import openapi
from ._solvers_api import SolversApi
from ._utils import PaginationGenerator

nest_asyncio.apply()  # allow to run coroutines via asyncio.run(coro)

__all__: Tuple[str, ...] = (
    # imports from osparc_client
    "__version__",
    "FilesApi",
    "PaginationGenerator",
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
    "StudiesApi",
    "OnePageSolverPort",
    "StudyPort",
    "Study",
    "JobMetadataUpdate",
    "Links",
    "SolverPort",
    "JobMetadata",
    "ErrorGet",
    "OnePageStudyPort",
    # imports from osparc
    "openapi",
)
