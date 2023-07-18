import json
import subprocess

import toml
import typer
from _utils import _CI_DIR, _PYPROJECT_TOML


def main() -> None:
    """Install the python client specified in the pyproject.toml"""
    client_config = toml.load(_PYPROJECT_TOML)["client"]
    install_bash: str = str(_CI_DIR / "install_osparc_python_client.bash")
    subprocess.run(["bash", install_bash, json.dumps(client_config)])


if __name__ == "__main__":
    typer.run(main)
