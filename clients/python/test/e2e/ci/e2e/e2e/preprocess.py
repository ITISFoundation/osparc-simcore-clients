import json
from pathlib import Path
from urllib.parse import urlparse

import pytest
import typer

from ._models import (
    Artifacts,
    ClientSettings,
    PytestConfig,
    PytestIniFile,
    ServerSettings,
)
from ._utils import handle_validation_error

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

    envs: list[str] = []
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
        "--capture=tee-sys "
        f"--html={html_log} --self-contained-html "
        f"--junitxml={junit_xml} --junit-prefix={junit_prefix}"
    )
    pytest_config: PytestConfig = PytestConfig(
        env="\n" + "\n".join(envs),
        required_plugins="pytest-env pytest-html pytest-asyncio",
        addopts=add_opts,
        asyncio_mode="auto",
        junit_logging="all",
        junit_log_passing_tests="True",
    )

    config: PytestIniFile = PytestIniFile(
        pytest=pytest_config, client=client_cfg, server=server_cfg, artifacts=artifacts
    )
    config.write_to_file(pth=test_dir / "pytest.ini")
    raise typer.Exit(code=pytest.ExitCode.OK)
