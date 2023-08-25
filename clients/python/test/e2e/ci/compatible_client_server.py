import pandas as pd
import pytest
import typer
from _data_classes import ClientConfig, PytestIniFile, ServerConfig
from _utils import _COMPATIBILITY_JSON, E2eExitCodes
from pydantic import ValidationError


def main() -> None:
    """Checks if the client x server configuration in the pyproject.toml
    is compatible

    Raises:
        typer.Exit: When exit code is returned
    """
    try:
        pytest_ini: PytestIniFile = PytestIniFile.read()
    except (ValueError, ValidationError):
        raise typer.Exit(code=E2eExitCodes.INVALID_JSON_DATA)

    client_cfg: ClientConfig = pytest_ini.client
    server_cfg: ServerConfig = pytest_ini.server
    if not _COMPATIBILITY_JSON.is_file():
        raise typer.Exit(code=E2eExitCodes.CI_SCRIPT_FAILURE)
    df: pd.DataFrame = pd.read_json(_COMPATIBILITY_JSON).T

    try:
        df = df[
            (df["server"] == server_cfg.url.netloc)
            & (df["client"] == client_cfg.compatibility_ref)
        ]
        if df.shape[0] != 1:
            raise RuntimeError(
                "Could not correctly determine compatibility between client and server."
            )
        is_compatible: bool = df["is_compatible"].loc[df.index[0]]
    except Exception:
        raise typer.Exit(code=E2eExitCodes.CI_SCRIPT_FAILURE)

    if not is_compatible:
        raise typer.Exit(code=E2eExitCodes.INCOMPATIBLE_CLIENT_SERVER)
    else:
        raise typer.Exit(code=pytest.ExitCode.OK)


if __name__ == "__main__":
    typer.run(main)
