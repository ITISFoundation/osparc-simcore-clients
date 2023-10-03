from pathlib import Path

import pandas as pd
import pytest
import typer
from _utils import E2eExitCodes
from postprocess_e2e import exit_code_valid


def exitcode_to_text(exitcode: int) -> str:
    """Turn exitcodes to string"""
    if exitcode in set(E2eExitCodes):
        return E2eExitCodes(exitcode).name
    elif exitcode in set(pytest.ExitCode):
        return pytest.ExitCode(exitcode).name
    else:
        raise typer.Exit(code=E2eExitCodes.CI_SCRIPT_FAILURE)


def make_pretty(entry: str):
    color: str
    if entry == E2eExitCodes.INCOMPATIBLE_CLIENT_SERVER.name:
        color = "#999999"
    elif entry == pytest.ExitCode.OK.name:
        color = "#99FF99"
    elif entry == pytest.ExitCode.TESTS_FAILED.name:
        color = "#FF9999"
    else:
        color = "#FF00FF"
    return "background-color: %s" % color


def main(e2e_artifacts_dir: str) -> None:
    """Generate html table"""
    artifacts: Path = Path(e2e_artifacts_dir)
    if not artifacts.is_dir():
        raise typer.Exit(code=E2eExitCodes.CI_SCRIPT_FAILURE)

    df: pd.DataFrame = pd.DataFrame()
    for file in artifacts.glob("*.json"):
        df = pd.concat([df, pd.read_json(file)], axis=1)

    for exit_code in df.to_numpy().flatten():
        if not exit_code_valid(exit_code):
            raise typer.Exit(code=E2eExitCodes.CI_SCRIPT_FAILURE)

    style = [
        {
            "selector": "*",
            "props": [
                ("border", "solid"),
                ("border-width", "0.1px"),
                ("border-collapse", "collapse"),
            ],
        },
        {"selector": "th", "props": [("background-color", "#F2F2F2")]},
    ]

    df = df.applymap(exitcode_to_text)
    s = df.style.applymap(make_pretty)
    s.set_table_attributes('style="font-size: 20px"')
    s.set_table_styles(style)
    s.set_caption("OSPARC e2e python client vs server tests")
    s.to_html(artifacts / "test_results.html")


if __name__ == "__main__":
    typer.run(main)
