import json
from pathlib import Path
from typing import List

import pytest
import typer
from _data_classes import (
    Artifacts,
    ClientConfig,
    PytestConfig,
    PytestIniFile,
    ServerConfig,
)
from _utils import _ARTIFACTS_DIR, E2eExitCodes
from pydantic import ValidationError


def main(client_config: str, server_config: str) -> None:
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

    html_log: Path = Path("../../") / (
        _ARTIFACTS_DIR
        / (client_cfg.client_ref + "_" + server_cfg.url.netloc)
        / f"pytest_{client_cfg.client_ref}_{server_cfg.url.netloc}.html"
    ).relative_to(Path("../../").resolve())
    add_opts: str = (
        "--tb=no --disable-warnings --no-header "
        f"--html={html_log} --self-contained-html"
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
    raise typer.Exit(code=pytest.ExitCode.OK)


if __name__ == "__main__":
    typer.run(main)
