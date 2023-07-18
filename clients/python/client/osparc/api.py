import warnings
from typing import Final

from ._warnings_and_errors import VisibleDeprecationWarning

warning_msg: Final[str] = (
    "osparc.api has been deprecated. Instead functionality within this module should be imported directly from osparc. "
    "I.e. please do 'from osparc import <fcn>' instead of 'from osparc.api import <fcn>'"
)
warnings.warn(warning_msg, VisibleDeprecationWarning)

from osparc_client.api import FilesApi, MetaApi, SolversApi, UsersApi

__all__ = ["FilesApi", "MetaApi", "SolversApi", "UsersApi"]
