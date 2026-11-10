import json
from pathlib import Path
from typing import Any


def openapi() -> dict[str, Any]:
    """
    Get openapi specification of automatically-generated part of this client
    """
    parsed: dict[str, Any] = json.loads(
        (Path(__file__).parent / "data" / "openapi.json").resolve().read_text()
    )
    return parsed
