import json
import subprocess

import typer
from _data_classes import PytestIniFile
from _utils import _CI_DIR, E2eExitCodes
from pydantic import ValidationError


def main() -> None:
    """Install the python client specified in the pyproject.toml"""
    try:
        pytest_ini: PytestIniFile = PytestIniFile.read()
    except (ValueError, ValidationError):
        raise typer.Exit(code=E2eExitCodes.INVALID_JSON_DATA)

    client_config = pytest_ini.client.model_dump(exclude_none=True)
    install_bash: str = str(_CI_DIR / "install_osparc_python_client.bash")
    subprocess.run(["bash", install_bash, json.dumps(client_config)])


if __name__ == "__main__":
    typer.run(main)
