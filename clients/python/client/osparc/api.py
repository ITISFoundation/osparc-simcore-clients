import warnings
from ._warnings_and_errors import VisibleDeprecationWarning

warn_msg:str = "osparc.api will be deprecated soon. Instead functionality within this module"
warn_msg += "should be imported directly from osparc. I.e. please do 'from osparc import <fcn>' instead of 'from osparc.api import <fcn>'"
warnings.warn(warn_msg, VisibleDeprecationWarning)

from osparc_client.api import (
    FilesApi,
    MetaApi,
    SolversApi,
    UsersApi
)


__all__ = [
    "FilesApi",
    "MetaApi",
    "SolversApi",
    "UsersApi"
]
