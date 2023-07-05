
import warnings
from ._warnings_and_errors import VisibleDeprecationWarning

warn_msg:str = "osparc.models will be deprecated soon. Instead functionality within this module"
warn_msg += "should be imported directly from osparc. I.e. please do 'from osparc import <fcn>' instead of 'from osparc.models import <fcn>'"
warnings.warn(warn_msg, VisibleDeprecationWarning)


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
