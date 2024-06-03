from uuid import UUID

from pydantic import Field
from pydantic_settings import BaseSettings


class ParentProjectInfo(BaseSettings):
    """Information a project cann pass onto its "children" (i.e. projects
    'spawned' through the api-server)"""

    x_simcore_parent_project_uuid: UUID | None = Field(
        alias="OSPARC_NODE_ID", default=None
    )
    x_simcore_parent_node_id: UUID | None = Field(alias="OSPARC_STUDY_ID", default=None)
