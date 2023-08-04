import warnings
from typing import Final, Tuple

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
)
from osparc_client.models import RunningState as TaskStates
from osparc_client.models import Solver, UserRoleEnum, UsersGroup, ValidationError

from ._warnings_and_errors import VisibleDeprecationWarning

warning_msg: Final[str] = (
    "osparc.models has been deprecated. Instead functionality within this module "
    "should be imported directly from osparc. I.e. please do 'from osparc import "
    "<fcn>' instead of 'from osparc.models import <fcn>'"
)
warnings.warn(warning_msg, VisibleDeprecationWarning)


__all__: Tuple[str, ...] = (
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
)
