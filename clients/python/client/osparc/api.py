import warnings

warn_msg:str = "osparc.api will be deprecated soon. Instead functionality within this module"
warn_msg += "should be imported directly from osparc. I.e. please do 'from osparc import <fcn>' instead of 'from osparc.api import <fcn>'"
warnings.warn(warn_msg, DeprecationWarning)

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
