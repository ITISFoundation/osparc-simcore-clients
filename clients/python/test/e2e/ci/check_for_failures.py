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
    artifacts.log_dir.mkdir(exist_ok=True)
    for pth in Path(artifacts.log_dir).glob("*.json"):
        df = pd.read_json(pth)
        df = df == pytest.ExitCode.TESTS_FAILED
        if df.to_numpy().flatten().any():
            raise typer.Exit(code=pytest.ExitCode.TESTS_FAILED)


if __name__ == "__main__":
    typer.run(main)
