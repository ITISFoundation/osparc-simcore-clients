from osparc_client import JobInputs as _JobInputs
from osparc_client import JobOutputs as _JobOutputs
from osparc_client import JobMetadata as _JobMetadata
from osparc_client import JobMetadataUpdate as _JobMetadataUpdate
from .models import File
from typing import Dict, Union, List, Optional
from pydantic import BaseModel, StrictStr, Field


class JobInputs(BaseModel):
    values: Dict[str, Union[File, List[object], bool, float, int, str, None]]

    def __init__(
        self, values: Dict[str, Union[File, List[object], bool, float, int, str, None]]
    ):
        super().__init__(values=values)


assert set(_JobInputs.model_fields.keys()) == set(JobInputs.model_fields.keys())


class JobOutputs(BaseModel):
    job_id: StrictStr = Field(description="Job that produced this output")
    results: Dict[str, Union[File, List[object], bool, float, int, str, None]]


assert set(_JobOutputs.model_fields.keys()) == set(JobOutputs.model_fields.keys())


class JobMetadata(BaseModel):
    job_id: StrictStr
    metadata: Dict[str, Union[bool, float, int, str, None]]
    url: Optional[str]


assert set(_JobMetadata.model_fields.keys()) == set(JobMetadata.model_fields.keys())


class JobMetadataUpdate(BaseModel):
    metadata: Dict[str, Union[bool, float, int, str, None]]


assert set(_JobMetadataUpdate.model_fields.keys()) == set(
    JobMetadataUpdate.model_fields.keys()
)
