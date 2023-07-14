from pathlib import Path
import typer
from _warnings_and_exit_codes import CiExitCodes
import pandas as pd
import pytest
from typing import Union

def exitcode_to_text(exitcode: int) -> str:
  """ Turn exitcodes to string
  """
  if exitcode == CiExitCodes.INVALID_CLIENT_VS_SERVER:
    return "incompatible"
  elif exitcode == pytest.ExitCode.OK:
    return "pass"
  elif exitcode == pytest.ExitCode.TESTS_FAILED:
     return "fail"
  else:
     raise typer.Exit(code=CiExitCodes.CI_SCRIPT_FAILURE)


def make_pretty(entry:str):
  color:str
  if entry == "incompatible":
    color = "grey"
  elif entry == "pass":
    color = "green"
  elif entry == "fail":
    color = "red"
  else:
     raise typer.Exit(code=CiExitCodes.CI_SCRIPT_FAILURE)
  return 'background-color: %s' % color

# def make_pretty(styler):
#   styler.set_caption("OSPARC public API client vs. server tests")
#   styler.format(exitcode_to_text)
#   styler.format_index(lambda v: v.strftime("%A"))
#   styler.background_gradient(axis=None, vmin=1, vmax=5, cmap="YlGnBu")
#   return styler

def main(e2e_artifacts_dir:str) -> None:
  """Generate html table
  """
  artifacts: Path = Path(e2e_artifacts_dir)
  if not artifacts.is_dir():
      raise typer.Exit(code=CiExitCodes.CI_SCRIPT_FAILURE)

  df: pd.DataFrame = pd.DataFrame()
  for file in artifacts.glob("*.json"):
      df = pd.concat([df, pd.read_json(file)], axis=1)

  df = df.applymap(exitcode_to_text)
  s = df.style.applymap(make_pretty)
  s.set_caption("OSPARC e2e python client vs server tests")
  s.to_html(artifacts / 'test_results.html')

if __name__ == '__main__':
   typer.run(main)
