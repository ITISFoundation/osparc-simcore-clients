import pandas as pd
import pytest
import toml
import typer
from _utils import (
    _COMPATIBILITY_JSON,
    _PYPROJECT_TOML,
    ClientConfig,
    E2eExitCodes,
    ServerConfig,
)
from pydantic import ValidationError


def main() -> None:
    """Checks if the client x server configuration in the pyproject.toml
    is compatible

    Raises:
        typer.Exit: When exit code is returned
    """
    try:
        pytest_envs = toml.load(_PYPROJECT_TOML)["tool"]["pytest"]["ini_options"]["env"]
        client_cfg: ClientConfig = ClientConfig(**toml.load(_PYPROJECT_TOML)["client"])
        server_cfg: ServerConfig = ServerConfig(
            **dict([tuple(s.strip(" ") for s in elm.split("=")) for elm in pytest_envs])
        )
    except (Exception, ValidationError) as e:
        print(e)
        raise typer.Exit(code=E2eExitCodes.INVALID_JSON_DATA)

    compatibility_df: pd.DataFrame = pd.read_json(_COMPATIBILITY_JSON)

    if client_cfg.compatibility_ref not in compatibility_df.columns:
        print(
            f"The client ref '{client_cfg.compatibility_ref}' could not "
            f"be found in {_COMPATIBILITY_JSON}"
        )
        raise typer.Exit(code=E2eExitCodes.INVALID_CLIENT_VS_SERVER)
    if server_cfg.url.netloc not in compatibility_df.index:
        print(
            f"The server netloc '{server_cfg.url.netloc}' could not "
            f"be found in {_COMPATIBILITY_JSON}"
        )

    if not compatibility_df[client_cfg.compatibility_ref][server_cfg.url.netloc]:
        raise typer.Exit(code=E2eExitCodes.INVALID_CLIENT_VS_SERVER)
    else:
        raise typer.Exit(code=pytest.ExitCode.OK)


if __name__ == "__main__":
    typer.run(main)
