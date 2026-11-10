from uuid import UUID

from pydantic import AliasChoices, AnyHttpUrl, Field, field_validator
from pydantic_settings import BaseSettings


class ParentProjectInfo(BaseSettings):
    """This is information a project can pass onto its "children" (i.e. projects
    'spawned' through the api-server)
    """

    x_simcore_parent_project_uuid: str | None = Field(
        alias="OSPARC_STUDY_ID", default=None
    )
    x_simcore_parent_node_id: str | None = Field(alias="OSPARC_NODE_ID", default=None)

    @field_validator("x_simcore_parent_project_uuid", "x_simcore_parent_node_id")
    @classmethod
    def _validate_uuids(cls, v: str | None) -> str | None:
        if v is not None:
            _ = UUID(v)
        return v


class ConfigurationEnvVars(BaseSettings):
    """Model for capturing env vars which should go into the Configuration"""

    # OSPARC_API_BASE_URL is the service-side name from
    # https://github.com/ITISFoundation/osparc-simcore/pull/5966, OSPARC_API_HOST the name
    # used before it. The ignore is for pydantic's mypy plugin rejecting a runtime alias.
    OSPARC_API_HOST: AnyHttpUrl = Field(  # type: ignore[pydantic-alias]
        default=...,
        validation_alias=AliasChoices("OSPARC_API_BASE_URL", "OSPARC_API_HOST"),
        description="OSPARC api url",
        examples=["https://api.osparc-master.speag.com/"],
    )
    OSPARC_API_KEY: str = Field(default=..., description="OSPARC api key")
    OSPARC_API_SECRET: str = Field(default=..., description="OSPARC api secret")


class OptionalConfigurationEnvVars(BaseSettings):
    """Per-field fallbacks for `Configuration` arguments left unset.

    Osparc injects these variables when starting a service (e.g. jupyter-math),
    so a `Configuration()` constructed without arguments resolves inside the
    service. Empty strings are treated as unset.
    """

    # OSPARC_API_BASE_URL is the service-side name from
    # https://github.com/ITISFoundation/osparc-simcore/pull/5966, OSPARC_API_HOST the name
    # used before it. The ignore is for pydantic's mypy plugin rejecting a runtime alias.
    OSPARC_API_HOST: AnyHttpUrl | None = Field(  # type: ignore[pydantic-alias]
        default=None,
        validation_alias=AliasChoices("OSPARC_API_BASE_URL", "OSPARC_API_HOST"),
        description="OSPARC api url",
        examples=["https://api.osparc-master.speag.com/"],
    )
    OSPARC_API_KEY: str | None = Field(
        default=None,
        validation_alias="OSPARC_API_KEY",
        description="OSPARC api key",
    )
    OSPARC_API_SECRET: str | None = Field(
        default=None,
        validation_alias="OSPARC_API_SECRET",
        description="OSPARC api secret",
    )

    @field_validator(
        "OSPARC_API_HOST", "OSPARC_API_KEY", "OSPARC_API_SECRET", mode="before"
    )
    @classmethod
    def _empty_string_is_unset(cls, value: object) -> object:
        return None if value == "" else value
