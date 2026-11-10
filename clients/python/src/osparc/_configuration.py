from collections.abc import Collection
from typing import Final

from osparc_client import Configuration as _Configuration
from urllib3 import Retry

from ._settings import OptionalConfigurationEnvVars

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

DEFAULT_HOST: Final[str] = "https://api.osparc.io"


class Configuration(_Configuration):
    def __init__(
        self,
        host: str | None = None,
        api_key: dict[str, str] | str | None = None,
        api_key_prefix: dict[str, str] | None = None,
        username: str | None = None,
        password: str | None = None,
        *,
        retry_max_count: int = 4,
        retry_methods: set[str] | None = None,
        retry_status_codes: set[int] | None = None,
        retry_backoff_factor: float = 4.0,
    ) -> None:
        """Arguments left unset fall back, per field, to the OSPARC_* env vars
        osparc injects into services; an unset host without env falls back to
        `DEFAULT_HOST`.
        """
        env_vars = OptionalConfigurationEnvVars()
        if host is None:
            # str(AnyHttpUrl) may keep a trailing slash, see
            # https://github.com/pydantic/pydantic/issues/7186
            host = (
                f"{env_vars.OSPARC_API_HOST}".rstrip("/")
                if env_vars.OSPARC_API_HOST
                else DEFAULT_HOST
            )
        if username is None:
            username = env_vars.OSPARC_API_KEY
        if password is None:
            password = env_vars.OSPARC_API_SECRET

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
