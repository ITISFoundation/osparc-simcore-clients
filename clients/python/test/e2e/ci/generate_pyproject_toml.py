import toml
from pathlib import Path
import pandas as pd
from urllib.parse import urlparse, ParseResult
from typing import List, Dict, Any, Union
import typer
from packaging import version
import json
from pydantic import ValidationError
import warnings
import pytest
from _utils import (E2eScriptFailure,
                     E2eExitCodes,
                     ClientConfig,
                     ServerConfig,
                     _PYPROJECT_TOML)


def main(client_config: str, server_config: str) -> None:
    """
    Generates a toml configuration file pytest e2e tests

    exceptions:
    -----------
        A typer.Exit(code=100) is raised if a failure is encountered

    returns:
    --------
        A bool indicating whether or not the (client, server) pair are compatible
    """
    # read in data
    try:
        client_cfg = ClientConfig(**json.loads(client_config))
        server_cfg = ServerConfig(**json.loads(server_config))
    except (ValidationError, ValueError) as e:
        print('\n\n'.join([client_config, server_config, str(e)]))
        typer.Exit(code=E2eExitCodes.INVALID_JSON_DATA)
        return

    _PYPROJECT_TOML.unlink(missing_ok=True)

    # set environment variables
    envs: List[str] = []
    envs.append(f"OSPARC_API_HOST = {server_cfg.url}")
    envs.append(f"OSPARC_API_KEY = {server_cfg.key}")
    envs.append(f"OSPARC_API_SECRET = {server_cfg.secret}")

    pytest_settings: Dict[str, Any] = {}
    pytest_settings["env"] = envs

    config: Dict[str, Any] = {}
    config["tool"] = {"pytest": {"ini_options": pytest_settings}}
    config["client"] = {"install_cmd": client_cfg.model_dump_json()}

    # generate toml file
    with open(str(_PYPROJECT_TOML), "w") as f:
        toml.dump(config, f)

    raise typer.Exit(code=pytest.ExitCode.OK)


if __name__ == "__main__":
    typer.run(main)
