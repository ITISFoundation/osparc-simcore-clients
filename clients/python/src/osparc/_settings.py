from typing import Optional
from uuid import UUID

from pydantic import AliasChoices, AnyHttpUrl, Field, field_validator
from pydantic_settings import BaseSettings


class ParentProjectInfo(BaseSettings):
    """This is information a project can pass onto its "children" (i.e. projects
    'spawned' through the api-server)
    """

    x_simcore_parent_project_uuid: Optional[str] = Field(
        alias="OSPARC_STUDY_ID", default=None
    )
    x_simcore_parent_node_id: Optional[str] = Field(
        alias="OSPARC_NODE_ID", default=None
    )

    @field_validator("x_simcore_parent_project_uuid", "x_simcore_parent_node_id")
    @classmethod
    def _validate_uuids(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            _ = UUID(v)
        return v


class ConfigurationEnvVars(BaseSettings):
    """Model for capturing env vars which should go into the Configuration"""

    # Service side: https://github.com/ITISFoundation/osparc-simcore/pull/5966
    OSPARC_API_HOST: AnyHttpUrl = Field(
        default=...,
        validation_alias=AliasChoices("OSPARC_API_BASE_URL", "OSPARC_API_HOST"),
        description="OSPARC api url",
        examples=["https://api.osparc-master.speag.com/"],
    )
    OSPARC_API_KEY: str = Field(default=..., description="OSPARC api key")
    OSPARC_API_SECRET: str = Field(default=..., description="OSPARC api secret")
