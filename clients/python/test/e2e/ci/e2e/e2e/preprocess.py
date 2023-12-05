import json
from pathlib import Path
from typing import List

import pandas as pd
import pytest
import typer
from pydantic import ValidationError

from ._data_classes import (
    Artifacts,
    ClientConfig,
    PytestConfig,
    PytestIniFile,
    ServerConfig,
)
from ._utils import _ARTIFACTS_DIR, _COMPATIBILITY_CSV, E2eExitCodes, print_line

cli = typer.Typer()


def log(client_cfg: ClientConfig, server_cfg: ServerConfig):
    """Log configuration"""
    print_line()
    print("Configuration")
    print("-------------")
    print(f"\tclient: {client_cfg.client_ref}")
    print(f"\tserver: {server_cfg.url.geturl()}")


@cli.command()
def generate_init_file(client_config: str, server_config: str) -> None:
    """
    Generates an ini configuration file for pytest e2e tests

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

    artifacts: Artifacts = Artifacts(
        artifact_dir=Path("../../")
        / _ARTIFACTS_DIR.relative_to(Path("../../").resolve()),
        result_data_frame=Path("../../")
        / _ARTIFACTS_DIR.relative_to(Path("../../").resolve())
        / (client_cfg.client_ref + ".json"),
        log_dir=Path("../../")
        / _ARTIFACTS_DIR.relative_to(Path("../../").resolve())
        / (client_cfg.client_ref + "_" + server_cfg.url.netloc),
    )

    envs: List[str] = []
    envs.append(f"OSPARC_API_HOST={server_cfg.url.geturl()}")
    envs.append(f"OSPARC_API_KEY={server_cfg.key}")
    envs.append(f"OSPARC_API_SECRET={server_cfg.secret}")
    envs.append(
        f"OSPARC_DEV_FEATURES_ENABLED=" f"{1 if client_cfg.client_dev_features else 0}"
    )

    html_log: Path = Path("../../") / (
        _ARTIFACTS_DIR
        / (client_cfg.client_ref + "_" + server_cfg.url.netloc)
        / f"pytest_{client_cfg.client_ref}_{server_cfg.url.netloc}.html"
    ).relative_to(Path("../../").resolve())
    junit_xml: Path = Path("../../") / (
        _ARTIFACTS_DIR
        / (client_cfg.client_ref + "_" + server_cfg.url.netloc)
        / f"junit_{client_cfg.client_ref}_{server_cfg.url.netloc}.xml"
    ).relative_to(Path("../../").resolve())
    junit_prefix: str = f"{client_cfg.client_ref}+{server_cfg.url.netloc}"
    add_opts: str = (
        f"--html={html_log} --self-contained-html "
        f"--junitxml={junit_xml} --junit-prefix={junit_prefix}"
    )
    pytest_config: PytestConfig = PytestConfig(
        env="\n" + "\n".join(envs),
        required_plugins="pytest-env pytest-html",
        addopts=add_opts,
    )

    config: PytestIniFile = PytestIniFile(
        pytest=pytest_config, client=client_cfg, server=server_cfg, artifacts=artifacts
    )
    config.generate()
    log(client_cfg, server_cfg)
    raise typer.Exit(code=pytest.ExitCode.OK)


@cli.command()
def check_server_client_compatibility() -> None:
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
    if not _COMPATIBILITY_CSV.is_file():
        raise typer.Exit(code=E2eExitCodes.CI_SCRIPT_FAILURE)
    df: pd.DataFrame = pd.read_csv(_COMPATIBILITY_CSV)

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
