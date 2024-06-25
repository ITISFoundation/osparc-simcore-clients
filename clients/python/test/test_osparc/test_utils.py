from typing import List

import pytest
from osparc._utils import ensure_unique_names


@pytest.mark.parametrize(
    "names,expected_names",
    [
        (["asd", "asd", "asdcsd", "kjbv"], ["asd", "asd(1)", "asdcsd", "kjbv"]),
        (
            ["asd", "asd", "asdcsd", "asdcsd", "asdcsd", "kjbv"],
            ["asd", "asd", "asdcsd", "asdcsd(1)", "asdcsd(2)", "kjbv"],
        ),
    ],
)
def test_ensure_unique_names(names: List[str], expected_names: List[str]):
    assert all(
        name == expected_name
        for name, expected_name in zip(ensure_unique_names(names), names)
    )
