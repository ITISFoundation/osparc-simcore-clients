from typing import Annotated, Dict, List
from uuid import UUID

from osparc_client import JobInputs as _JobInputs
from osparc_client import JobMetadata as _JobMetadata
from osparc_client import JobMetadataUpdate as _JobMetadataUpdate
from osparc_client import JobOutputs as _JobOutputs
from pydantic import BaseModel, BeforeValidator, Field, StrictStr

from .models import File


def _ensure_str(v: UUID | str) -> str:
    if isinstance(v, UUID):
        v = f"{v}"
    return v


class JobInputs(BaseModel):
    values: Dict[str, File | List[object] | bool | float | int | str | None]

    def __init__(
        self, values: Dict[str, File | List[object] | bool | float | int | str | None]
    ):
        super().__init__(values=values)


assert set(_JobInputs.model_fields.keys()) == set(JobInputs.model_fields.keys())  # nosec


class JobOutputs(BaseModel):
    job_id: Annotated[
        StrictStr,
        Field(description="Job that produced this output"),
        BeforeValidator(_ensure_str),
    ]
    results: Dict[str, File | List[object] | bool | float | int | str | None]


assert set(_JobOutputs.model_fields.keys()) == set(JobOutputs.model_fields.keys())  # nosec


class JobMetadata(BaseModel):
    job_id: Annotated[StrictStr, BeforeValidator(_ensure_str)]
    metadata: Dict[str, bool | float | int | str | None]
    url: str | None


assert set(_JobMetadata.model_fields.keys()) == set(JobMetadata.model_fields.keys())  # nosec


class JobMetadataUpdate(BaseModel):
    metadata: Dict[str, bool | float | int | str | None]


assert set(_JobMetadataUpdate.model_fields.keys()) == set(
    JobMetadataUpdate.model_fields.keys()
)  # nosec
