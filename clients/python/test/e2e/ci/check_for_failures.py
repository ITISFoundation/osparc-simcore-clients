from pathlib import Path

import pandas as pd
import pytest
import typer
from _data_classes import Artifacts, PytestIniFile
from _utils import E2eExitCodes
from pydantic import ValidationError


def main():
    """Loop through all json artifacts and fail in case of testfailure"""
    try:
        pytest_ini: PytestIniFile = PytestIniFile.read()
    except (ValueError, ValidationError):
        raise typer.Exit(code=E2eExitCodes.CI_SCRIPT_FAILURE)

    artifacts: Artifacts = pytest_ini.artifacts
    if not artifacts.log_dir.is_dir():
        raise typer.Exit(code=E2eExitCodes.CI_SCRIPT_FAILURE)
    result_jsons = list(Path(artifacts.artifact_dir).glob("*.json"))
    if not len(result_jsons):
        raise typer.Exit(code=E2eExitCodes.CI_SCRIPT_FAILURE)
    for pth in result_jsons:
        df = pd.read_json(pth)
        df = (df != pytest.ExitCode.OK) & (
            df != E2eExitCodes.INCOMPATIBLE_CLIENT_SERVER
        )
        if df.to_numpy().flatten().any():
            raise typer.Exit(code=pytest.ExitCode.TESTS_FAILED)


if __name__ == "__main__":
    typer.run(main)
