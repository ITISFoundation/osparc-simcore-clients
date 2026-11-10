from typing import Annotated, Dict, List, TypeAlias
from uuid import UUID

from osparc_client import JobInputs as _JobInputs
from osparc_client import JobMetadata as _JobMetadata
from osparc_client import JobMetadataUpdate as _JobMetadataUpdate
from osparc_client import JobOutputs as _JobOutputs
from osparc_client.models.file import File
from pydantic import BaseModel, BeforeValidator, Field, StrictStr


def _ensure_str(v: UUID | str) -> str:
    if isinstance(v, UUID):
        v = f"{v}"
    return v


# One entry of `JobInputs.values`/`JobOutputs.results`. openapi-generator emitted a
# `ValuesValue` model for this union until v7.27.0, which inlines it as `Any`.
ValuesValue: TypeAlias = File | List[object] | bool | float | int | str | None


class JobInputs(BaseModel):
    values: Dict[str, ValuesValue]

    def __init__(self, values: Dict[str, ValuesValue]):
        super().__init__(values=values)


assert set(_JobInputs.model_fields.keys()) == set(JobInputs.model_fields.keys())  # nosec


class JobOutputs(BaseModel):
    job_id: Annotated[
        StrictStr,
        Field(description="Job that produced this output"),
        BeforeValidator(_ensure_str),
    ]
    results: Dict[str, ValuesValue]


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
