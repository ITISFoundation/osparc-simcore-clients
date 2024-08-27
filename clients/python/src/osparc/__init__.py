import warnings
from platform import python_version
from typing import List, Tuple

import nest_asyncio
from osparc_client import (
    ApiException,
    ApiKeyError,
    ApiTypeError,
    ApiValueError,
    BodyUploadFileV0FilesContentPut,
    Configuration,
    CreditsApi,
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
    Solver,
    SolverPort,
    UserRoleEnum,
    UsersApi,
    UsersGroup,
    ValidationError,
    __version__,
)
from osparc_client import RunningState as TaskStates
from packaging.version import Version

from ._api_client import ApiClient
from ._exceptions import RequestError, VisibleDeprecationWarning
from ._files_api import FilesApi
from ._info import openapi
from ._solvers_api import SolversApi
from ._studies_api import StudiesApi
from ._utils import dev_features_enabled

_PYTHON_VERSION_RETIRED = Version("3.8.0")
_PYTHON_VERSION_DEPRECATED = Version("3.8.0")
assert _PYTHON_VERSION_RETIRED <= _PYTHON_VERSION_DEPRECATED  # nosec

if Version(python_version()) < _PYTHON_VERSION_RETIRED:
    error_msg: str = (
        f"Python version {python_version()} is retired for this version of osparc. "
        f"Please use Python version {_PYTHON_VERSION_DEPRECATED}."
    )
    raise RuntimeError(error_msg)

if Version(python_version()) < _PYTHON_VERSION_DEPRECATED:
    warning_msg: str = (
        f"Python {python_version()} is deprecated. "
        "Please upgrade to "
        f"Python version >= {_PYTHON_VERSION_DEPRECATED}."
    )
    warnings.warn(warning_msg, VisibleDeprecationWarning)


nest_asyncio.apply()  # allow to run coroutines via asyncio.run(coro)

dev_features: List[str] = []
if dev_features_enabled():
    dev_features = [
        "JobMetadata",
        "JobMetadataUpdate",
        "Links",
        "OnePageStudyPort",
        "PaginationGenerator",
        "Study",
        "StudyPort",
    ]

__all__: Tuple[str, ...] = tuple(dev_features) + (
    "__version__",
    "ApiClient",
    "ApiException",
    "ApiKeyError",
    "ApiTypeError",
    "ApiValueError",
    "BodyUploadFileV0FilesContentPut",
    "Configuration",
    "CreditsApi",
    "ErrorGet",
    "File",
    "FilesApi",
    "Groups",
    "HTTPValidationError",
    "Job",
    "JobInputs",
    "JobOutputs",
    "JobStatus",
    "Meta",
    "MetaApi",
    "OnePageSolverPort",
    "openapi",
    "OpenApiException",
    "Profile",
    "ProfileUpdate",
    "RequestError",
    "Solver",
    "SolverPort",
    "SolversApi",
    "StudiesApi",
    "TaskStates",
    "UserRoleEnum",
    "UsersApi",
    "UsersGroup",
    "ValidationError",
)  # type: ignore
