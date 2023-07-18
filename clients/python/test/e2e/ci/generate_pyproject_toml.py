import json
from typing import Any, List

import pytest
import toml
import typer
from _utils import _PYPROJECT_TOML, ClientConfig, E2eExitCodes, ServerConfig
from pydantic import ValidationError


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
        print("\n\n".join([client_config, server_config, str(e)]))
        raise typer.Exit(code=E2eExitCodes.INVALID_JSON_DATA)

    _PYPROJECT_TOML.unlink(missing_ok=True)

    # set environment variables
    envs: List[str] = []
    envs.append(f"OSPARC_API_HOST = {server_cfg.url.geturl()}")
    envs.append(f"OSPARC_API_KEY = {server_cfg.key}")
    envs.append(f"OSPARC_API_SECRET = {server_cfg.secret}")

    pytest_settings: dict[str, Any] = {}
    pytest_settings["env"] = envs

    config: dict[str, Any] = {}
    config["tool"] = {"pytest": {"ini_options": pytest_settings}}
    config["client"] = client_cfg.model_dump()
    config["server"] = server_cfg.model_dump()

    # generate toml file
    with open(str(_PYPROJECT_TOML), "w") as f:
        toml.dump(config, f)

    raise typer.Exit(code=pytest.ExitCode.OK)


if __name__ == "__main__":
    typer.run(main)
