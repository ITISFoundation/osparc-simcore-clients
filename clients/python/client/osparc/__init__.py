from typing import List, Tuple

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

from ._exceptions import RequestError
from ._files_api import FilesApi
from ._info import openapi
from ._solvers_api import SolversApi
from ._utils import dev_features_enabled

nest_asyncio.apply()  # allow to run coroutines via asyncio.run(coro)

dev_features: List[str] = []
if dev_features_enabled():
    dev_features = [
        "PaginationGenerator",
        "StudiesApi",
        "StudyPort",
        "Study",
        "JobMetadataUpdate",
        "Links",
        "JobMetadata",
        "OnePageStudyPort",
    ]

__all__: Tuple[str, ...] = tuple(dev_features) + (
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
    "openapi",
    "RequestError",
)  # type: ignore
