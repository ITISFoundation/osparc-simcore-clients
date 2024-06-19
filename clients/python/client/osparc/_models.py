from typing import Optional
from uuid import UUID

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class ParentProjectInfo(BaseSettings):
    """Information a project cann pass onto its "children" (i.e. projects
    'spawned' through the api-server)"""

    x_simcore_parent_project_uuid: Optional[str] = Field(
        alias="OSPARC_STUDY_ID", default=None
    )
    x_simcore_parent_node_id: Optional[str] = Field(
        alias="OSPARC_NODE_ID", default=None
    )

    @field_validator("x_simcore_parent_project_uuid", "x_simcore_parent_node_id")
    @classmethod
    def _validate_uuids(cls, v: Optional[str]) -> str:
        if v is not None:
            _ = UUID(v)
        return v
