import toml
import typer
from pathlib import Path
from typing import Dict, List, Set
import pandas as pd
from urllib.parse import urlparse
import shutil
import json
from _utils import E2eExitCodes, E2eScriptFailure
import pytest
import warnings

# pyproject.toml keys
surl: str = "OSPARC_API_HOST"
skey: str = "OSPARC_API_KEY"
ssecret: str = "OSPARC_API_SECRET"
skeys: List[str] = [surl, skey, ssecret]

crepo: str = "OSPARC_CLIENT_REPO"
cbranch: str = "OSPARC_CLIENT_BRANCH"
cversion: str = "OSPARC_CLIENT_VERSION"
ckeys: List[str] = [crepo, cbranch, cversion]


def extract_val(toml_entry: List[str], key: str) -> str:
    entries: List[str] = [elm for elm in toml_entry if key in elm]
    if not len(entries) == 1:
        warnings.warn(f"toml_entry={toml_entry}", E2eScriptFailure)
        raise typer.Exit(code=E2eExitCodes.CI_SCRIPT_FAILURE)
    return entries[0].replace(key, "").strip(" =")


def main(exit_code: int) -> None:
    """
    Postprocess results from e2e pytests
    This scripts appends the pytest exit code to clients/python/artifacts/e2e/<client_ref>.json for it to be parsed later
    It also moves the pyproject.toml to clients/python/artifacts/e2e in order to be able to reproduce tests later

    arguments:
    ----------
        exit_code : Integer exit code from running pytests or a custom exitcode (see ExitCodes).

    returns:
    --------
        None
    """
    expected_exitcodes: Set = {
        E2eExitCodes.INVALID_CLIENT_VS_SERVER,
        pytest.ExitCode.OK,
        pytest.ExitCode.TESTS_FAILED,
    }
    if not exit_code in expected_exitcodes:
        warnings.warn(
            f"Received unexpected exitcode {exit_code}. See https://docs.pytest.org/en/7.1.x/reference/exit-codes.html",
            E2eScriptFailure,
        )
    artifact_dir: Path = (
        Path(__file__).parent.parent.parent.parent / "artifacts" / "e2e"
    )
    cfg_file: Path = Path(__file__).parent.parent / "pyproject.toml"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    if not cfg_file.is_file():
        warnings.warn(f"cfg_file={cfg_file}", E2eScriptFailure)
        raise typer.Exit(code=E2eExitCodes.CI_SCRIPT_FAILURE)

    # extract values
    pytest_cfg: Dict = toml.load(cfg_file)["tool"]["pytest"]["ini_options"]
    client_cfg: Dict[str, str] = json.loads(
        toml.load(cfg_file)["client"]["install_cmd"]
    )
    if not isinstance(client_cfg, dict):
        raise typer.Exit(code=E2eExitCodes.CI_SCRIPT_FAILURE)
    branch: str = client_cfg[cbranch]
    version: str = client_cfg[cversion]
    envs: List[str] = pytest_cfg["env"]
    if not isinstance(envs, list):
        raise typer.Exit(code=E2eExitCodes.CI_SCRIPT_FAILURE)
    url: str = extract_val(envs, surl)

    # add result to json
    client_ref: str = branch + version
    result_file: Path = artifact_dir / (client_ref + ".json")
    new_df: pd.DataFrame = pd.DataFrame(
        columns=[client_ref], index=[urlparse(url).netloc], data=[exit_code]
    )
    result_df: pd.DataFrame
    if result_file.is_file():
        result_df = pd.read_json(result_file)
        result_df = pd.concat([result_df, new_df], axis=0, verify_integrity=True)
        result_file.unlink(missing_ok=False)
    else:
        result_df = new_df
    result_file.write_text(result_df.to_json())

    # copy toml to artifacts dir
    toml_dir: Path = artifact_dir / (client_ref + "+" + urlparse(url).netloc)
    toml_dir.mkdir(exist_ok=False)
    shutil.move(cfg_file, toml_dir / cfg_file.name)
    raise typer.Exit(code=pytest.ExitCode.OK)


if __name__ == "__main__":
    typer.run(main)