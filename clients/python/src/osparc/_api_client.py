# wraps osparc_client.api_client

from typing import Optional

from osparc_client.api_client import ApiClient as _ApiClient
from ._configuration import Configuration
from pydantic import ValidationError
from ._settings import ConfigurationEnvVars


class ApiClient(_ApiClient):
    def __init__(
        self,
        configuration: Optional[Configuration] = None,
        header_name=None,
        header_value=None,
        cookie=None,
    ):
        if configuration is None:
            try:
                env_vars = ConfigurationEnvVars()
                configuration = Configuration(
                    host=f"{env_vars.OSPARC_API_HOST}".rstrip(
                        "/"
                    ),  # https://github.com/pydantic/pydantic/issues/7186
                    username=env_vars.OSPARC_API_KEY,
                    password=env_vars.OSPARC_API_SECRET,
                )
            except ValidationError as exc:
                raise RuntimeError(
                    f"Could not initialize configuration from environment (expected {ConfigurationEnvVars.model_fields_set}). "
                    "If your osparc host, key and secret are not exposed as "
                    "environment variables you must construct the "
                    "osparc.Configuration object explicitly"
                ) from exc

        super().__init__(configuration, header_name, header_value, cookie)
