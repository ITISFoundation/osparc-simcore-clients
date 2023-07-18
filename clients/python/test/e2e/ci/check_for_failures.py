from pathlib import Path

import pandas as pd
import pytest
import typer
from _utils import E2eExitCodes


def main(e2e_artifacts_dir: str):
    """Loop through all json artifacts and fail in case of testfailure"""
    artifacts = Path(e2e_artifacts_dir)
    if not artifacts.is_dir():
        typer.Exit(code=E2eExitCodes.CI_SCRIPT_FAILURE)
    for pth in Path(artifacts).glob("*.json"):
        df = pd.read_json(pth)
        df = df == pytest.ExitCode.TESTS_FAILED
        if df.to_numpy().flatten().any():
            raise typer.Exit(code=pytest.ExitCode.TESTS_FAILED)


if __name__ == "__main__":
    typer.run(main)
