import json
from pathlib import Path
from typing import List
from urllib.parse import urlparse

import pandas as pd
import pytest
import typer

from ._models import (
    Artifacts,
    ClientSettings,
    PytestConfig,
    PytestIniFile,
    ServerSettings,
)
from ._utils import _COMPATIBILITY_CSV, E2eExitCodes, handle_validation_error

cli = typer.Typer()


@cli.command()
@handle_validation_error
def generate_ini(
    artifacts_dir: Path, test_dir: Path, client_config: str, server_config: str
) -> None:
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
    client_cfg = ClientSettings(**json.loads(client_config))
    server_cfg = ServerSettings(**json.loads(server_config))

    host_netloc = urlparse(server_cfg.host).netloc
    artifacts: Artifacts = Artifacts(
        artifact_dir=artifacts_dir,
        result_data_frame=artifacts_dir / (client_cfg.ref + ".json"),
        log_dir=artifacts_dir / (client_cfg.ref + "_" + host_netloc),
    )
    artifacts.artifact_dir.mkdir(parents=True, exist_ok=True)
    artifacts.log_dir.mkdir(parents=True, exist_ok=True)

    envs: List[str] = []
    envs.append(f"OSPARC_API_HOST={urlparse(server_cfg.host).geturl()}")
    envs.append(f"OSPARC_API_KEY={server_cfg.key.get_secret_value()}")
    envs.append(f"OSPARC_API_SECRET={server_cfg.secret.get_secret_value()}")

    html_log = (
        artifacts_dir
        / (client_cfg.ref + "_" + host_netloc)
        / f"pytest_{client_cfg.ref}_{host_netloc}.html"
    )
    junit_xml = (
        artifacts_dir
        / (client_cfg.ref + "_" + host_netloc)
        / f"junit_{client_cfg.ref}_{host_netloc}.xml"
    )
    junit_prefix: str = f"{client_cfg.ref}+{host_netloc}"
    add_opts: str = (
        f"--html={html_log} --self-contained-html "
        f"--junitxml={junit_xml} --junit-prefix={junit_prefix}"
    )
    pytest_config: PytestConfig = PytestConfig(
        env="\n" + "\n".join(envs),
        required_plugins="pytest-env pytest-html pytest-asyncio",
        addopts=add_opts,
        asyncio_mode="auto",
    )

    config: PytestIniFile = PytestIniFile(
        pytest=pytest_config, client=client_cfg, server=server_cfg, artifacts=artifacts
    )
    config.write_to_file(pth=test_dir / "pytest.ini")
    raise typer.Exit(code=pytest.ExitCode.OK)


@cli.command()
@handle_validation_error
def check_compatibility() -> None:
    """Checks if the client x server configuration in the pyproject.toml
    is compatible

    Raises:
        typer.Exit: When exit code is returned
    """
    pytest_ini: PytestIniFile = PytestIniFile.create_from_file()
    client_cfg: ClientSettings = pytest_ini.client
    server_cfg: ServerSettings = pytest_ini.server
    if not _COMPATIBILITY_CSV.is_file():
        typer.echo("Invalid compatibility csv")
        raise typer.Exit(code=E2eExitCodes.CI_SCRIPT_FAILURE, err=True)
    df: pd.DataFrame = pd.read_csv(_COMPATIBILITY_CSV)
    try:
        df = df[
            (df["server"] == urlparse(server_cfg.host).netloc)
            & (df["client"] == client_cfg.compatibility_ref)
        ]
        if df.shape[0] != 1:
            raise RuntimeError(
                "Could not correctly determine compatibility between client and server."
            )
        is_compatible: bool = df["is_compatible"].loc[df.index[0]]
    except Exception as exc:
        typer.echo(f"{exc}", err=True)
        raise typer.Exit(code=E2eExitCodes.CI_SCRIPT_FAILURE)

    if not is_compatible:
        raise typer.Exit(code=E2eExitCodes.SKIPPING_TESTS)
    else:
        raise typer.Exit(code=pytest.ExitCode.OK)
