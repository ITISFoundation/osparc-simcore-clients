# coding: utf-8

# flake8: noqa

"""
    osparc.io web API

    osparc-simcore public web API specifications  # noqa: E501

    The version of the OpenAPI document: 0.3.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

__version__ = "0.4.1"

# import apis into sdk package
from osparc.api.files_api import FilesApi
from osparc.api.meta_api import MetaApi
from osparc.api.solvers_api import SolversApi
from osparc.api.users_api import UsersApi

# import ApiClient
from osparc.api_client import ApiClient
from osparc.configuration import Configuration
from osparc.exceptions import OpenApiException
from osparc.exceptions import ApiTypeError
from osparc.exceptions import ApiValueError
from osparc.exceptions import ApiKeyError
from osparc.exceptions import ApiException
# import models into sdk package
from osparc.models.body_upload_file_v0_files_content_put import BodyUploadFileV0FilesContentPut
from osparc.models.file import File
from osparc.models.groups import Groups
from osparc.models.http_validation_error import HTTPValidationError
from osparc.models.job import Job
from osparc.models.job_inputs import JobInputs
from osparc.models.job_outputs import JobOutputs
from osparc.models.job_status import JobStatus
from osparc.models.meta import Meta
from osparc.models.profile import Profile
from osparc.models.profile_update import ProfileUpdate
from osparc.models.solver import Solver
from osparc.models.task_states import TaskStates
from osparc.models.user_role_enum import UserRoleEnum
from osparc.models.users_group import UsersGroup
from osparc.models.validation_error import ValidationError

