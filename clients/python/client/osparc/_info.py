import json
from pathlib import Path
from typing import Any, Dict


def openapi() -> Dict[str, Any]:
    """
    Get openapi specification of automatically-generated part of this client
    """
    return json.loads(
        (Path(__file__).parent / "data" / "openapi.json").resolve().read_text()
    )
