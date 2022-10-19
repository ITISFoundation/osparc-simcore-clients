# PATCH file
from contextlib import suppress
from typing import Any, Callable, Union

from .file import File

AnyOfFilenumberintegerbooleanstring = Union[File, float, int, bool, str]


def deserialize_any_of(
    data: Any,
    deserialize_func: Callable,
):
    for klass in [File, float, int, bool, str]:
        with suppress(Exception):
            return deserialize_func(data, klass)
    raise ValueError(f"Cannot deserialize {data}")
