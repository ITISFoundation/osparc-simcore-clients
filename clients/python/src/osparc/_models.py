from osparc_client import ValuesValue
from osparc_client import JobInputs as _JobInputs
from osparc_client import JobOutputs as _JobOutputs
from typing import Dict, Any
from pydantic import BaseModel, StrictStr, Field


def _values_dict(v: Dict[str, Any]) -> Dict[str, ValuesValue | None]:
    result = {}
    for k, v in v.items():
        if v is not None:
            result[k] = ValuesValue(v)
        else:
            result[k] = v
    return result


class JobInputs(_JobInputs):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0:
            input = args[0]
            assert isinstance(input, dict)
            super().__init__(values=_values_dict(input))
            return
        if len(args) == 0 and len(kwargs) == 1:
            values = kwargs.get("values")
            if values is None:
                raise RuntimeError("When passing a single kwarg it must be 'values'")
            super().__init__(values=_values_dict(values))
            return
        else:
            super().__init__(*args, **kwargs)


class JobOutputs(BaseModel):
    job_id: StrictStr = Field(description="Job that produced this output")
    results: Dict[str, Any]

    @classmethod
    def from_osparc_client_job_outputs(cls, outputs: _JobOutputs) -> "JobOutputs":
        _results = {}
        for k, v in outputs.results.items():
            if isinstance(v, ValuesValue):
                _results[k] = v.actual_instance
            else:
                _results[k] = v

        return cls(job_id=outputs.job_id, results=_results)
