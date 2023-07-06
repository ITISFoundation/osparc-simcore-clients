
import warnings
from ._warnings_and_errors import VisibleDeprecationWarning

warnings.warn(
    "osparc.models has been deprecated. Instead functionality within this module should be imported directly from osparc. I.e. please do 'from osparc import <fcn>' instead of 'from osparc.models import <fcn>'"
    , VisibleDeprecationWarning)


from osparc_client.models import (
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
    ValidationError
)

__all__ = [
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
    "ValidationError"
]
