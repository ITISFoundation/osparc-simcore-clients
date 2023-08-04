import warnings
from typing import Final, Tuple

from osparc_client.api import FilesApi, MetaApi, SolversApi, UsersApi

from ._warnings_and_errors import VisibleDeprecationWarning

warning_msg: Final[str] = (
    "osparc.api has been deprecated. Instead functionality within this module "
    "should be imported directly from osparc. I.e. please do 'from osparc import "
    "<fcn>' instead of 'from osparc.api import <fcn>'"
)
warnings.warn(warning_msg, VisibleDeprecationWarning)


__all__: Tuple[str, ...] = ("FilesApi", "MetaApi", "SolversApi", "UsersApi")
