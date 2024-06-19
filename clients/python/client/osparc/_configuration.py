import os
from typing import Set

from osparc_client.configuration import Configuration

# Monkey patches __init__
original_init = Configuration.__init__


def new_init(
    self,
    host=None,
    api_key=None,
    api_key_prefix=None,
    username=None,
    password=None,
    signing_info=None,
    *,
    retry_max_count: int = 4,
    retry_methods: Set[str] = ...,
    retry_status_codes: Set[int] = ...,
    retry_backoff_factor=4
):
    # SEE https://github.com/ITISFoundation/osparc-simcore/issues/5925
    host = host or os.environ.get("OSPARC_API_BASE_URL", "https://api.osparc.io")
    username = username or os.environ.get("OSPARC_API_KEY")
    password = password or os.environ.get("OSPARC_API_SECRET")

    original_init(
        self,
        host,
        api_key,
        api_key_prefix,
        username,
        password,
        signing_info,
        retry_max_count=retry_max_count,
        retry_methods=retry_methods,
        retry_status_codes=retry_status_codes,
        retry_backoff_factor=retry_backoff_factor,
    )


Configuration.__init__ = new_init
