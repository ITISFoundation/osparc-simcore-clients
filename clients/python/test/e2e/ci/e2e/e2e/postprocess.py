import warnings
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import osparc
import pandas as pd
import pytest
import typer

from ._data_classes import Artifacts, ClientConfig, PytestIniFile, ServerConfig
from ._utils import E2eExitCodes, E2eScriptFailure, handle_validation_error

cli = typer.Typer()


def log(exit_code: int):
    """Log exit status"""
    config = PytestIniFile.read()
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
    pytest_ini: PytestIniFile = PytestIniFile.read()
    client_cfg: ClientConfig = pytest_ini.client
    server_cfg: ServerConfig = pytest_ini.server
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
    pytest_ini.write(artifacts.log_dir / "pytest.ini")
    raise typer.Exit(code=pytest.ExitCode.OK)


@cli.command()
@handle_validation_error
def check_for_failure():
    """Loop through all json artifacts and fail in case of testfailure"""
    pytest_ini: PytestIniFile = PytestIniFile.read()
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
    if entry == E2eExitCodes.INCOMPATIBLE_CLIENT_SERVER.name:
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
    for file in artifacts.glob("*.json"):
        df = pd.concat([df, pd.read_json(file)], axis=1)

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

    df = df.applymap(_exitcode_to_text)
    s = df.style.applymap(_make_pretty)
    s.set_table_attributes('style="font-size: 20px"')
    s.set_table_styles(style)
    s.set_caption("OSPARC e2e python client vs server tests")
    s.to_html(artifacts / "test_results.html")


@cli.command()
def log_dir(pytest_ini: Optional[Path] = None):
    ini = PytestIniFile.read(pytest_ini) if pytest_ini else PytestIniFile.read()
    typer.echo(ini.artifacts.log_dir)


@cli.command()
def clean_up_jobs(artifacts_dir: Path):
    """Loop through all users defined in pytest.ini files
    in artifacts_dir and stop+delete all jobs.
    """
    if not artifacts_dir.is_dir():
        typer.echo(f"{artifacts_dir=} is not a directory", err=True)
        raise typer.Exit(code=E2eExitCodes.INVALID_JSON_DATA)
    for pytest_ini in artifacts_dir.rglob("*pytest.ini"):
        server_config = PytestIniFile.read(pytest_ini).server
        config = osparc.Configuration(
            host=server_config.host,
            username=server_config.key,
            password=server_config.secret,
        )
        typer.echo(
            f"Cleaning up jobs for user:\n{server_config.model_dump_json(indent=1)}"
        )
        with osparc.ApiClient(config) as api_client:
            solvers_api = osparc.SolversApi(api_client)
            assert isinstance(solvers := solvers_api.list_solvers_releases(), list)
            for solver in solvers:
                assert isinstance(solver, osparc.Solver)
                assert (id_ := solver.id) is not None
                assert (version := solver.version) is not None
                for job in solvers_api.jobs(id_, version):
                    assert isinstance(job, osparc.Job)
                    assert isinstance(
                        job_status := solvers_api.inspect_job(id_, version, job.id),
                        osparc.JobStatus,
                    )
                    if job_status.stopped_at is None:
                        solvers_api.stop_job(id_, version, job.id)
                    solvers_api.delete_job(id_, version, job.id)
