import json
import shutil
import warnings
from pathlib import Path
from typing import List, Set
from urllib.parse import urlparse

import pandas as pd
import pytest
import toml
import typer
from _utils import (
    _ARTIFACTS_DIR,
    _PYPROJECT_TOML,
    ClientConfig,
    E2eExitCodes,
    E2eScriptFailure,
    ServerConfig,
)
from pydantic import ValidationError


def main(exit_code: int) -> None:
    """
    Postprocess results from e2e pytests
    This scripts appends the pytest exit code to clients/python/artifacts/e2e/<client_ref>.json for it to be parsed later
    It also moves the pyproject.toml to clients/python/artifacts/e2e in order to be able to reproduce tests later

    arguments:
    ----------
        exit_code : Integer exit code from running pytests or a custom exitcode (see ExitCodes).

    returns:
    --------
        None
    """
    expected_exitcodes: Set = {
        E2eExitCodes.INVALID_CLIENT_VS_SERVER,
        pytest.ExitCode.OK,
        pytest.ExitCode.TESTS_FAILED,
    }
    if not exit_code in expected_exitcodes:
        warnings.warn(
            f"Received unexpected exitcode {exit_code}. See https://docs.pytest.org/en/7.1.x/reference/exit-codes.html",
            E2eScriptFailure,
        )
        typer.Exit(code=E2eExitCodes.CI_SCRIPT_FAILURE)

    _ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    if not _PYPROJECT_TOML.is_file():
        warnings.warn(f"cfg_file={_PYPROJECT_TOML}", E2eScriptFailure)
        raise typer.Exit(code=E2eExitCodes.CI_SCRIPT_FAILURE)

    # extract values
    try:
        server_cfg: ServerConfig = ServerConfig(**toml.load(_PYPROJECT_TOML)["server"])
        client_cfg: ClientConfig = ClientConfig(**toml.load(_PYPROJECT_TOML)["client"])
    except (ValueError, ValidationError) as e:
        print(toml.load(_PYPROJECT_TOML)["server"])
        print(print(toml.load(_PYPROJECT_TOML)["client"]))
        raise typer.Exit(code=E2eExitCodes.INVALID_JSON_DATA)

    # add result to json
    result_file: Path = _ARTIFACTS_DIR / (client_cfg.client_ref + ".json")
    new_df: pd.DataFrame = pd.DataFrame(
        columns=[client_cfg.client_ref], index=[server_cfg.url.netloc], data=[exit_code]
    )
    result_df: pd.DataFrame
    if result_file.is_file():
        result_df = pd.read_json(result_file)
        result_df = pd.concat([result_df, new_df], axis=0, verify_integrity=True)
        result_file.unlink(missing_ok=False)
    else:
        result_df = new_df
    result_file.write_text(result_df.to_json())

    # copy toml to artifacts dir
    toml_dir: Path = _ARTIFACTS_DIR / (
        client_cfg.client_ref + "+" + server_cfg.url.netloc
    )
    toml_dir.mkdir(exist_ok=False)
    shutil.move(_PYPROJECT_TOML, toml_dir / _PYPROJECT_TOML.name)
    raise typer.Exit(code=pytest.ExitCode.OK)


if __name__ == "__main__":
    typer.run(main)
