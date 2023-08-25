from pathlib import Path

import pandas as pd
import pytest
import typer
from _utils import E2eExitCodes


def exitcode_to_text(exitcode: int) -> str:
    """Turn exitcodes to string"""
    if exitcode == E2eExitCodes.INCOMPATIBLE_CLIENT_SERVER:
        return "incompatible"
    elif exitcode == pytest.ExitCode.OK:
        return "pass"
    elif exitcode == pytest.ExitCode.TESTS_FAILED:
        return "fail"
    else:
        raise typer.Exit(code=E2eExitCodes.CI_SCRIPT_FAILURE)


def make_pretty(entry: str):
    color: str
    if entry == "incompatible":
        color = "#999999"
    elif entry == "pass":
        color = "#99FF99"
    elif entry == "fail":
        color = "#FF9999"
    else:
        raise typer.Exit(code=E2eExitCodes.CI_SCRIPT_FAILURE)
    return "background-color: %s" % color


def main(e2e_artifacts_dir: str) -> None:
    """Generate html table"""
    artifacts: Path = Path(e2e_artifacts_dir)
    if not artifacts.is_dir():
        raise typer.Exit(code=E2eExitCodes.CI_SCRIPT_FAILURE)

    df: pd.DataFrame = pd.DataFrame()
    for file in artifacts.glob("*.json"):
        df = pd.concat([df, pd.read_json(file)], axis=1)
    any_failure: bool = bool(
        (df == pytest.ExitCode.TESTS_FAILED).to_numpy().flatten().any()
    )

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
    raise typer.Exit(
        code=pytest.ExitCode.TESTS_FAILED if any_failure else pytest.ExitCode.OK
    )


if __name__ == "__main__":
    typer.run(main)
