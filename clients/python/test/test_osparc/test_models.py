from typing import get_args
from uuid import UUID, uuid4

from osparc.models import File, JobInputs, JobOutputs, ValuesValue


def test_values_value_covers_every_type_the_api_documents():
    assert set(get_args(ValuesValue)) == {
        File,
        list[object],
        bool,
        float,
        int,
        str,
        type(None),
    }


def test_job_values_keep_every_documented_type():
    file = File(id=UUID(f"{uuid4()}"), filename="notes.txt")
    values = {
        "an-int": 1,
        "a-float": 1.5,
        "a-str": "hello",
        "a-bool": True,
        "a-list": [1, 2],
        "a-none": None,
        "a-file": file,
    }

    inputs = JobInputs(values)
    assert inputs.values == values

    outputs = JobOutputs(job_id=f"{uuid4()}", results=values)
    assert outputs.results["a-file"].filename == file.filename
