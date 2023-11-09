import warnings
from pathlib import Path

import pandas as pd
import pytest
import typer
from _data_classes import Artifacts, ClientConfig, PytestIniFile, ServerConfig
from _utils import E2eExitCodes, E2eScriptFailure, print_line
from pydantic import ValidationError


def log(exit_code: int):
    """Log exit status"""
    print("Exit status")
    print("-------------")
    if exit_code in {e.value for e in E2eExitCodes}:
        print(f"\t{E2eExitCodes(exit_code).name}")
    elif exit_code in {e.value for e in pytest.ExitCode}:
        print(f"\t{pytest.ExitCode(exit_code).name}")
    else:
        print(f"\t{E2eExitCodes.CI_SCRIPT_FAILURE.name}")
    print_line()


def exit_code_valid(exit_code: int) -> bool:
    if exit_code not in set(pytest.ExitCode).union(E2eExitCodes):
        warnings.warn(
            f"Received unexpected exitcode {exit_code}. See https://docs.pytest.org/en/7.1.x/reference/exit-codes.html",
            E2eScriptFailure,
        )
        return False
    return True


def main(exit_code: int) -> None:
    """
    Postprocess results from e2e pytests
    This scripts appends the pytest exit code to
    clients/python/artifacts/e2e/<client_ref>.json for it to be parsed later.
    It also moves the pyproject.toml to clients/python/artifacts/e2e in order
    to be able to reproduce tests later

    arguments:
    ----------
        exit_code : Integer exit code from running pytests or a
        custom exitcode (see ExitCodes).

    returns:
    --------
        None
    """
    log(exit_code)
    if not exit_code_valid(exit_code):
        raise typer.Exit(code=E2eExitCodes.CI_SCRIPT_FAILURE)

    # get config
    try:
        pytest_ini: PytestIniFile = PytestIniFile.read()
    except (ValueError, ValidationError):
        raise typer.Exit(code=E2eExitCodes.INVALID_JSON_DATA)

    client_cfg: ClientConfig = pytest_ini.client
    server_cfg: ServerConfig = pytest_ini.server
    artifacts: Artifacts = pytest_ini.artifacts

    # add result to json
    result_file: Path = artifacts.result_data_frame
    result_file.parent.mkdir(exist_ok=True, parents=True)
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

    # copy ini to artifacts dir
    artifacts.log_dir.mkdir(exist_ok=True)
    pytest_ini.generate(artifacts.log_dir / "pytest.ini")
    raise typer.Exit(code=pytest.ExitCode.OK)


if __name__ == "__main__":
    typer.run(main)
