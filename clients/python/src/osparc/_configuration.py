import os
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

DEFAULT_HOST: Final = "https://api.osparc.io"

# Same names as ConfigurationEnvVars in _settings.py: OSPARC_API_BASE_URL is
# the service-side name from osparc-simcore#5966, OSPARC_API_HOST the legacy one.
_HOST_ENV_NAMES: Final = ("OSPARC_API_BASE_URL", "OSPARC_API_HOST")
_USERNAME_ENV_NAME: Final = "OSPARC_API_KEY"
_PASSWORD_ENV_NAME: Final = "OSPARC_API_SECRET"


def _first_env(names: Collection[str]) -> str | None:
    for name in names:
        if value := os.environ.get(name):
            return value
    return None


class Configuration(_Configuration):
    def __init__(
        self,
        host: str | None = None,
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
        # osparc injects OSPARC_* env vars when starting a service (e.g.
        # jupyter-math); use them as per-field fallbacks so Configuration()
        # works there without arguments, while explicit arguments win.
        if host is None:
            env_host = _first_env(_HOST_ENV_NAMES)
            host = env_host.rstrip("/") if env_host else DEFAULT_HOST
        if username is None:
            username = _first_env((_USERNAME_ENV_NAME,))
        if password is None:
            password = _first_env((_PASSWORD_ENV_NAME,))

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
