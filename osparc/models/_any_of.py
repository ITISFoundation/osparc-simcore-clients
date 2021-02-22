from contextlib import suppress
from typing import Any, Callable, List, Union

from .file import File

AnyOfFilenumberintegerstring = Union[File, float, int, str]

def deserialize_any_of(
    data: Any,
    deserialize_func: Callable,
):
    for klass in [File, float, int, str]:
        with suppress(Exception):
            return deserialize_func(data, klass)
    raise ValueError(f"Cannot deserialize {data}")
