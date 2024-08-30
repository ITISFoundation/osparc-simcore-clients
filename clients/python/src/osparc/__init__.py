import warnings
from platform import python_version
from typing import Tuple

import nest_asyncio
from osparc_client import RunningState as TaskStates
from osparc_client import (
    __version__,
)
from osparc_client.api.credits_api import CreditsApi
from osparc_client.api.meta_api import MetaApi
from osparc_client.api.users_api import UsersApi
from osparc_client.api.wallets_api import WalletsApi
from osparc_client.configuration import Configuration
from osparc_client.models.body_abort_multipart_upload_v0_files_file_id_abort_post import (
    BodyAbortMultipartUploadV0FilesFileIdAbortPost,
)
from osparc_client.models.body_complete_multipart_upload_v0_files_file_id_complete_post import (
    BodyCompleteMultipartUploadV0FilesFileIdCompletePost,
)
from osparc_client.models.body_upload_file_v0_files_content_put import (
    BodyUploadFileV0FilesContentPut,
)
from osparc_client.models.client_file import ClientFile
from osparc_client.models.client_file_upload_data import ClientFileUploadData
from osparc_client.models.error_get import ErrorGet
from osparc_client.models.file import File
from osparc_client.models.file_upload_completion_body import FileUploadCompletionBody
from osparc_client.models.file_upload_data import FileUploadData
from osparc_client.models.get_credit_price import GetCreditPrice
from osparc_client.models.groups import Groups
from osparc_client.models.http_validation_error import HTTPValidationError
from osparc_client.models.job import Job
from osparc_client.models.job_inputs import JobInputs
from osparc_client.models.job_log import JobLog
from osparc_client.models.job_logs_map import JobLogsMap
from osparc_client.models.job_metadata import JobMetadata
from osparc_client.models.job_metadata_update import JobMetadataUpdate
from osparc_client.models.job_outputs import JobOutputs
from osparc_client.models.job_status import JobStatus
from osparc_client.models.links import Links
from osparc_client.models.log_link import LogLink
from osparc_client.models.meta import Meta
from osparc_client.models.one_page_solver_port import OnePageSolverPort
from osparc_client.models.one_page_study_port import OnePageStudyPort
from osparc_client.models.page_file import PageFile
from osparc_client.models.page_job import PageJob
from osparc_client.models.page_solver import PageSolver
from osparc_client.models.page_study import PageStudy
from osparc_client.models.pricing_plan_classification import PricingPlanClassification
from osparc_client.models.pricing_unit_get import PricingUnitGet
from osparc_client.models.profile import Profile
from osparc_client.models.profile_update import ProfileUpdate
from osparc_client.models.running_state import RunningState
from osparc_client.models.service_pricing_plan_get import ServicePricingPlanGet
from osparc_client.models.solver import Solver
from osparc_client.models.solver_port import SolverPort
from osparc_client.models.study import Study
from osparc_client.models.study_port import StudyPort
from osparc_client.models.upload_links import UploadLinks
from osparc_client.models.uploaded_part import UploadedPart
from osparc_client.models.user_role_enum import UserRoleEnum
from osparc_client.models.users_group import UsersGroup
from osparc_client.models.validation_error import ValidationError
from osparc_client.models.wallet_get_with_available_credits import (
    WalletGetWithAvailableCredits,
)
from osparc_client.models.wallet_status import WalletStatus
from packaging.version import Version

from ._api_client import ApiClient
from ._api_files_api import FilesApi
from ._api_solvers_api import SolversApi
from ._api_studies_api import StudiesApi
from ._exceptions import RequestError, VisibleDeprecationWarning
from ._info import openapi

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


__all__: Tuple[str, ...] = (
    "__version__",
    "ApiClient",
    "BodyAbortMultipartUploadV0FilesFileIdAbortPost",
    "BodyCompleteMultipartUploadV0FilesFileIdCompletePost",
    "BodyUploadFileV0FilesContentPut",
    "ClientFile",
    "ClientFileUploadData",
    "Configuration",
    "CreditsApi",
    "ErrorGet",
    "File",
    "FilesApi",
    "FileUploadCompletionBody",
    "FileUploadData",
    "GetCreditPrice",
    "Groups",
    "HTTPValidationError",
    "Job",
    "JobInputs",
    "JobLog",
    "JobLogsMap",
    "JobMetadata",
    "JobMetadataUpdate",
    "JobOutputs",
    "JobStatus",
    "Links",
    "LogLink",
    "Meta",
    "MetaApi",
    "OnePageSolverPort",
    "OnePageStudyPort",
    "openapi",
    "PageFile",
    "PageJob",
    "PageSolver",
    "PageStudy",
    "PricingPlanClassification",
    "PricingUnitGet",
    "Profile",
    "ProfileUpdate",
    "RequestError",
    "RunningState",
    "ServicePricingPlanGet",
    "Solver",
    "SolverPort",
    "SolversApi",
    "StudiesApi",
    "Study",
    "StudyPort",
    "TaskStates",
    "UploadedPart",
    "UploadLinks",
    "UserRoleEnum",
    "UsersApi",
    "UsersGroup",
    "ValidationError",
    "Version",
    "VisibleDeprecationWarning",
    "WalletGetWithAvailableCredits",
    "WalletStatus",
    "WalletsApi",
)  # type: ignore
