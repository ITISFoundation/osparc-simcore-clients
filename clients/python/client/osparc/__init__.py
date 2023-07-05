"""
0.5.0 osparc client
"""
import sys
import warnings

from ._info import openapi
from osparc_client import (
    ApiClient,
    Configuration,
    OpenApiException,
    ApiTypeError,
    ApiValueError,
    ApiKeyError,
    ApiException,
    # model imports
    BodyUploadFileV0FilesContentPut,
    File,
    Groups,
    HTTPValidationError,
    Job,
    JobInputs,
    JobOutputs,
    JobStatus,
    Meta,
    Profile,
    ProfileUpdate,
    Solver,
    TaskStates,
    UserRoleEnum,
    UsersGroup,
    ValidationError,
    # api imports
    FilesApi,
    MetaApi,
    SolversApi,
    UsersApi
)

__all__ = [
    # imports from osparc_client
    "api",
    "models",
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
    # imports from osparc
    "openapi"
]
