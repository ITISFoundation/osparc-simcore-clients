import pytest
from _warnings_and_exit_codes import CiExitCodes
from pathlib import Path
import typer
import pandas as pd

def main(e2e_artifacts_dir:str):
  """Loop through all json artifacts and fail in case of testfailure
  """
  artifacts = Path(e2e_artifacts_dir)
  if not artifacts.is_dir():
    typer.Exit(code=CiExitCodes.CI_SCRIPT_FAILURE)
  for pth in Path(artifacts).glob("*.json"):
    df = pd.read_json(pth)
    df = df == pytest.ExitCode.TESTS_FAILED
    if df.to_numpy().flatten().any():
      typer.Exit(code=pytest.ExitCode.TESTS_FAILED)
    else:
      typer.Exit(code=CiExitCodes.OK)



if __name__ == '__main__':
    typer.run(main)
