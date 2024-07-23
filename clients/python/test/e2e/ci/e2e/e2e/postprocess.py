import configparser
import warnings
from datetime import timedelta
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import osparc
import pandas as pd
import pytest
import typer
from pydantic import PositiveInt
from tenacity import (
    RetryError,
    Retrying,
    retry_if_exception_type,
    stop_after_attempt,
    stop_after_delay,
)
from urllib3.exceptions import HTTPError as Urllib3HttpError

from ._models import Artifacts, ClientSettings, PytestIniFile, ServerSettings
from ._utils import E2eExitCodes, E2eScriptFailure, handle_validation_error

cli = typer.Typer()


def log(exit_code: int):
    """Log exit status"""
    config = PytestIniFile.create_from_file()
    n_dash = 100
    typer.echo(n_dash * "=")
    typer.echo("\nServer config")
    typer.echo("-------------")
    typer.echo(config.server.model_dump_json(indent=1))
    typer.echo("\nClient config")
    typer.echo("-------------")
    typer.echo(config.client.model_dump_json(indent=1))
    typer.echo("\nExit status")
    typer.echo("-------------")
    if exit_code in {e.value for e in E2eExitCodes}:
        typer.echo(f"\t{E2eExitCodes(exit_code).name}")
    elif exit_code in {e.value for e in pytest.ExitCode}:
        typer.echo(f"\t{pytest.ExitCode(exit_code).name}")
    else:
        typer.echo(f"\t{E2eExitCodes.CI_SCRIPT_FAILURE.name}")
    typer.echo("\n" + n_dash * "=")


def _exit_code_valid(exit_code: int) -> bool:
    if exit_code not in set(pytest.ExitCode).union(E2eExitCodes):
        warnings.warn(
            f"Received unexpected exitcode {exit_code}. See https://docs.pytest.org/en/7.1.x/reference/exit-codes.html",
            E2eScriptFailure,
        )
        return False
    return True


@cli.command()
@handle_validation_error
def single_testrun(exit_code: int) -> None:
    """
    Postprocess results from e2e pytests
    Appends the pytest exit code to
    clients/python/artifacts/e2e/<client_ref>.json for it to be parsed later.
    It also moves the pytest.ini to clients/python/artifacts/e2e in order
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
    if not _exit_code_valid(exit_code):
        raise typer.Exit(code=E2eExitCodes.CI_SCRIPT_FAILURE)

    # get config
    pytest_ini: PytestIniFile = PytestIniFile.create_from_file()
    client_cfg: ClientSettings = pytest_ini.client
    server_cfg: ServerSettings = pytest_ini.server
    artifacts: Artifacts = pytest_ini.artifacts

    # add result to json
    result_file: Path = artifacts.result_data_frame
    result_file.parent.mkdir(exist_ok=True, parents=True)
    new_df: pd.DataFrame = pd.DataFrame(
        columns=[client_cfg.ref],
        index=[urlparse(server_cfg.host).netloc],
        data=[exit_code],
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
    pytest_ini.write_to_file(artifacts.log_dir / "pytest.ini")
    raise typer.Exit(code=pytest.ExitCode.OK)


@cli.command()
@handle_validation_error
def check_for_failure(e2e_artifacts_dir: str):
    """Loop through all json artifacts and fail in case of testfailure"""
    artifacts: Path = Path(e2e_artifacts_dir)
    if not artifacts.is_dir():
        raise typer.Exit(code=E2eExitCodes.CI_SCRIPT_FAILURE)
    count = 0
    for pth in artifacts.glob("*.json"):
        count += 1
        df = pd.read_json(pth)
        df = (df != pytest.ExitCode.OK) & (df != E2eExitCodes.SKIPPING_TESTS)
        if df.to_numpy().flatten().any():
            raise typer.Exit(code=pytest.ExitCode.TESTS_FAILED)
    if count == 0:
        raise typer.Exit(code=E2eExitCodes.CI_SCRIPT_FAILURE)


def _exitcode_to_text(exitcode: int) -> str:
    """Turn exitcodes to string"""
    if exitcode in set(E2eExitCodes):
        return E2eExitCodes(exitcode).name
    elif exitcode in set(pytest.ExitCode):
        return pytest.ExitCode(exitcode).name
    else:
        raise typer.Exit(code=E2eExitCodes.CI_SCRIPT_FAILURE)


def _make_pretty(entry: str):
    color: str
    if entry == E2eExitCodes.SKIPPING_TESTS.name:
        color = "#999999"
    elif entry == pytest.ExitCode.OK.name:
        color = "#99FF99"
    elif entry == pytest.ExitCode.TESTS_FAILED.name:
        color = "#FF9999"
    else:
        color = "#FF00FF"
    return "background-color: %s" % color


@cli.command()
def generate_html_table(e2e_artifacts_dir: str) -> None:
    """Generate html table"""
    artifacts: Path = Path(e2e_artifacts_dir)
    if not artifacts.is_dir():
        raise typer.Exit(code=E2eExitCodes.CI_SCRIPT_FAILURE)

    df: pd.DataFrame = pd.DataFrame()
    for path in artifacts.glob("*.json"):
        df = pd.concat([df, pd.read_json(path)], axis=1)

    for exit_code in df.to_numpy().flatten():
        if not _exit_code_valid(exit_code):
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

    df = df.map(_exitcode_to_text)
    df = df.reindex(sorted(df.columns), axis=1)  # Sort columns alphabetically
    s = df.style.map(_make_pretty)
    s.set_table_attributes('style="font-size: 20px"')
    s.set_table_styles(style)
    s.set_caption("OSPARC e2e python client vs server tests")
    s.to_html(artifacts / "test_results.html")
    df.rename_axis("OSPARC e2e python client vs server test")
    typer.echo(df.to_markdown(tablefmt="double_grid"))


@cli.command()
def log_dir(pytest_ini: Optional[Path] = None):
    ini = (
        PytestIniFile.create_from_file(pytest_ini)
        if pytest_ini
        else PytestIniFile.create_from_file()
    )
    typer.echo(ini.artifacts.log_dir)


@cli.command()
def clean_up_jobs(artifacts_dir: Path, retry_minutes: Optional[PositiveInt] = None):
    """Loop through all users defined in pytest.ini files
    in artifacts_dir and stop+delete all jobs.
    """
    if not artifacts_dir.is_dir():
        typer.echo(f"{artifacts_dir=} is not a directory", err=True)
        raise typer.Exit(code=E2eExitCodes.INVALID_JSON_DATA)
    servers: set[ServerSettings] = set()
    for pytest_ini in artifacts_dir.rglob("*pytest.ini"):
        obj = configparser.ConfigParser()
        obj.read(pytest_ini)
        cfg = {s: dict(obj.items(s)) for s in obj.sections()}
        server_config = ServerSettings.model_validate(cfg.get("server"))
        servers.add(server_config)
    for server_config in servers:
        config = osparc.Configuration(
            host=server_config.host,
            username=server_config.key.get_secret_value(),
            password=server_config.secret.get_secret_value(),
        )
        msg = "Cleaning up jobs for user: "
        msg += f"\n{server_config.model_dump_json(indent=1)}"
        typer.echo(msg)
        try:
            for attempt in Retrying(
                retry=retry_if_exception_type((osparc.ApiException, Urllib3HttpError)),
                stop=stop_after_delay(timedelta(minutes=retry_minutes))
                if retry_minutes
                else stop_after_attempt(1),
            ):
                with attempt:
                    with osparc.ApiClient(config) as api_client:
                        solvers_api = osparc.SolversApi(api_client)
                        assert isinstance(
                            solvers := solvers_api.list_solvers_releases(), list
                        )
                        for solver in solvers:
                            assert isinstance(solver, osparc.Solver)
                            assert (id_ := solver.id) is not None
                            assert (version := solver.version) is not None
                            for job in solvers_api.jobs(id_, version):
                                assert isinstance(job, osparc.Job)
                                solvers_api.delete_job(id_, version, job.id)
        except RetryError as exc:
            typer.echo(
                typer.style(
                    (
                        "Failed when cleaning jobs when encountering "
                        f"the following exception:\n{exc.last_attempt.exception()}"
                    ),
                    fg=typer.colors.RED,
                    bold=True,
                )
            )
