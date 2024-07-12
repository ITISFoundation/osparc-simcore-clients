from typing import Optional

from osparc_client import ApiClient as _ApiClient
from osparc_client import Configuration
from pydantic import ValidationError

from ._models import ConfigurationModel


class ApiClient(_ApiClient):
    def __init__(
        self,
        configuration: Optional[Configuration] = None,
        header_name=None,
        header_value=None,
        cookie=None,
        pool_threads=1,
    ):
        if configuration is None:
            try:
                env_vars = ConfigurationModel()
                configuration = Configuration(
                    host=f"{env_vars.OSPARC_API_HOST}".rstrip(
                        "/"
                    ),  # https://github.com/pydantic/pydantic/issues/7186
                    username=env_vars.OSPARC_API_KEY,
                    password=env_vars.OSPARC_API_SECRET,
                )
            except ValidationError as exc:
                raise RuntimeError(
                    "Could not initialize configuration from environment. "
                    "If your osparc host, key and secret are not exposed as "
                    "environment variables you must construct the "
                    "Configuration object explicitly"
                ) from exc

        super().__init__(configuration, header_name, header_value, cookie, pool_threads)
