import toml
from pathlib import Path
import pandas as pd
from urllib.parse import urlparse, ParseResult
from typing import List, Dict, Any, Union
import typer
from packaging import version
import json
from _warnings_and_exit_codes import CiScriptFailure, CiExitCodes
import warnings

# keys to be found in input dicts
surl: str = "OSPARC_API_HOST"
skey: str = "OSPARC_API_KEY"
ssecret: str = "OSPARC_API_SECRET"
skeys: List[str] = [surl, skey, ssecret]

crepo: str = "OSPARC_CLIENT_REPO"
cbranch: str = "OSPARC_CLIENT_BRANCH"
cversion: str = "OSPARC_CLIENT_VERSION"
ckeys: List[str] = [crepo, cbranch, cversion]


def main(client_config: str, server_config: str) -> bool:
    """
    Generates a toml configuration file pytest e2e tests

    exceptions:
    -----------
        A typer.Exit(code=100) is raised if a failure is encountered

    returns:
    --------
        A bool indicating whether or not the (client, server) pair are compatible
    """
    # read in data
    ccfg = json.loads(client_config)
    scfg = json.loads(server_config)
    if not isinstance(ccfg, dict):
        warnings.warn(
            f"The client configuration received in {__file__} was invalid",
            CiScriptFailure,
        )
        typer.Exit(code=CiExitCodes.CI_SCRIPT_FAILURE)
    if not isinstance(scfg, dict):
        warnings.warn(
            f"The server configuration received in {__file__} was invalid",
            CiScriptFailure,
        )
        typer.Exit(code=CiExitCodes.CI_SCRIPT_FAILURE)
    if not all(key in skeys for key in scfg.keys()):
        warnings.warn(
            f"The following server inputs are required: {skeys}. Received: {set(scfg.keys())}",
            CiScriptFailure,
        )
        typer.Exit(code=CiExitCodes.CI_SCRIPT_FAILURE)

    osparc_url: ParseResult = urlparse(scfg[surl])
    ini_file: Path = Path(__file__).parent.parent / "pyproject.toml"
    ini_file.unlink(missing_ok=True)
    comp_df: pd.DataFrame = pd.read_json(
        Path(__file__).parent.parent / "data" / "server_client_compatibility.json"
    )

    # sanity check client inputs
    if not (ccfg[cbranch] == "" or ccfg[cversion] == ""):
        warnings.warn(
            f"{cbranch}={ccfg[cbranch]}, {cversion}={ccfg[cversion]}", CiScriptFailure
        )
        raise typer.Exit(code=CiExitCodes.CI_SCRIPT_FAILURE)
    # sanity checks
    if ccfg[cversion] != "" and ccfg[cversion] != "latest":
        _ = version.parse(ccfg[cversion])
    if ccfg[cbranch] != "":
        if ccfg[crepo] == "":
            warnings.warn(
                f"{cbranch}={ccfg[cbranch]}, {crepo}={ccfg[crepo]}", CiScriptFailure
            )
            raise typer.Exit(code=CiExitCodes.CI_SCRIPT_FAILURE)

    # set environment variables
    envs: List[str] = []
    envs.append(f"OSPARC_API_HOST = {scfg[surl]}")
    envs.append(f"OSPARC_API_KEY = {scfg[skey]}")
    envs.append(f"OSPARC_API_SECRET = {scfg[ssecret]}")

    pytest_settings: Dict[str, Any] = {}
    pytest_settings["env"] = envs

    config: Dict[str, Any] = {}
    config["tool"] = {"pytest": {"ini_options": pytest_settings}}
    config["client"] = {"install_cmd": json.dumps(json.loads(client_config))}
    # generate toml file
    with open(str(ini_file), "w") as f:
        toml.dump(config, f)

    # check client vs server compatibility
    client_ref = ccfg[cbranch] + ccfg[cversion]
    if not client_ref in comp_df.keys():
        warnings.warn(
            f"invalid client_ref: {client_ref}.\nValid ones are: {comp_df.keys()}",
            CiScriptFailure,
        )
    if not osparc_url.netloc in comp_df.index:
        warnings.warn(
            f"invalid server_url: {osparc_url.netloc}\nValid ones are: {list(comp_df.index)}",
            CiScriptFailure,
        )

    is_compatible: bool = comp_df[client_ref][osparc_url.netloc]
    raise typer.Exit(
        code=CiExitCodes.OK if is_compatible else CiExitCodes.INVALID_CLIENT_VS_SERVER
    )


if __name__ == "__main__":
    typer.run(main)
