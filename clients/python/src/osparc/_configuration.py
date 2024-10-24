from osparc_client import Configuration as _Configuration
from typing import Set
from urllib3 import Retry


class Configuration(_Configuration):
    def __init__(
        self,
        host="https://api.osparc.io",
        api_key=None,
        api_key_prefix=None,
        username=None,
        password=None,
        *,
        retry_max_count: int = 4,
        retry_methods: Set[str] = {
            "DELETE",
            "GET",
            "HEAD",
            "OPTIONS",
            "PUT",
            "TRACE",
            "POST",
            "PATCH",
            "CONNECT",
        },
        retry_status_codes: Set[int] = {429, 503, 504},
        retry_backoff_factor=4.0,
    ):
        retries = Retry(
            total=retry_max_count,
            backoff_factor=retry_backoff_factor,
            status_forcelist=retry_status_codes,
            allowed_methods=retry_methods,
            respect_retry_after_header=True,
            raise_on_status=True,
        )
        super().__init__(
            host=host,
            api_key=api_key,
            api_key_prefix=api_key_prefix,
            username=username,
            password=password,
            retries=retries,
        )
