from collections.abc import Collection
from typing import Final

from osparc_client import Configuration as _Configuration
from urllib3 import Retry

# Module-level: a default set literal is created once and would be shared, and
# mutated, across all instances
_DEFAULT_RETRY_METHODS: Final = frozenset(
    {
        "DELETE",
        "GET",
        "HEAD",
        "OPTIONS",
        "PUT",
        "TRACE",
        "POST",
        "PATCH",
        "CONNECT",
    }
)
_DEFAULT_RETRY_STATUS_CODES: Final = frozenset({429, 503, 504})


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
        retry_methods: set[str] | None = None,
        retry_status_codes: set[int] | None = None,
        retry_backoff_factor=4.0,
    ):
        methods: Collection[str] = (
            _DEFAULT_RETRY_METHODS if retry_methods is None else retry_methods
        )
        status_codes: Collection[int] = (
            _DEFAULT_RETRY_STATUS_CODES
            if retry_status_codes is None
            else retry_status_codes
        )
        retries = Retry(
            total=retry_max_count,
            backoff_factor=retry_backoff_factor,
            status_forcelist=status_codes,
            allowed_methods=methods,
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
