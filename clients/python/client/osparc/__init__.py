import warnings
from platform import python_version
from typing import Final, List, Tuple

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
from packaging.version import Version

from ._exceptions import RequestError, VisibleDeprecationWarning
from ._files_api import FilesApi
from ._info import openapi
from ._solvers_api import SolversApi
from ._studies_api import StudiesApi
from ._utils import dev_features_enabled

if Version(python_version()) < Version("3.8.0"):
    warning_msg: Final[str] = (
        "This is the final version of osparc which "
        f"will support Python {python_version()}. "
        "Future versions of osparc will only support Python version >=3.8.0."
    )
    warnings.warn(warning_msg, VisibleDeprecationWarning)


nest_asyncio.apply()  # allow to run coroutines via asyncio.run(coro)

dev_features: List[str] = []
if dev_features_enabled():
    dev_features = [
        "PaginationGenerator",
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
    "StudiesApi",
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
