import toml
from pathlib import Path
import pandas as pd
from urllib.parse import urlparse, ParseResult
from typing import List, Dict, Any, Union
import typer
from packaging import version
import json

# keys to be found in input dicts
surl: str = 'OSPARC_API_HOST'
skey: str = 'OSPARC_API_KEY'
ssecret: str = 'OSPARC_API_SECRET'
skeys: List[str] = [surl,skey,ssecret]

crepo: str = 'OSPARC_CLIENT_REPO'
cbranch: str = 'OSPARC_CLIENT_BRANCH'
cversion: str = 'OSPARC_CLIENT_VERSION'
ckeys: List[str] = [crepo, cbranch, cversion]



def main(
    ccfg: Union[str,Dict[str,str]], scfg: Union[str,Dict[str,str]]
) -> bool:
    """
    Generates a toml configuration file pytest e2e tests

    returns:
    --------
        A bool indicating whether or not the (client, server) pair are compatible
    """
    # read in data
    if isinstance(ccfg,str):
        ccfg = json.loads(ccfg)
    if isinstance(scfg,str):
        scfg = json.loads(scfg)
    assert isinstance(ccfg,dict)
    assert isinstance(scfg,dict)
    assert len(set(ccfg.keys())-set(ckeys)) == 0, f"the following client inputs were missing: {set(ccfg.keys())-set(ckeys)}"
    assert len(set(scfg.keys())-set(skeys)) == 0, f"the following servr inputs were missing: {set(scfg.keys())-set(skeys)}"

    osparc_url: ParseResult = urlparse(scfg[surl])
    ini_file: Path = Path(__file__).parent / "pyproject.toml"
    ini_file.unlink(missing_ok=True)
    comp_df: pd.DataFrame = pd.read_json(
        Path(__file__).parent / "data" / "server_client_compatibility.json"
    )

    # sanity check client inputs
    assert (ccfg[cbranch] == "" or ccfg[cversion] == ""), f"{cbranch}={ccfg[cbranch]}, {cversion}={ccfg[cversion]}"
    # sanity checks
    if ccfg[cversion] != "":
        _ = version.parse(ccfg[cversion])
    if ccfg[cbranch] != "":
        assert ccfg[crepo] != "", f"{cbranch}={ccfg[cbranch]}, {crepo}={ccfg[crepo]}"

    # set environment variables
    envs: List[str] = []
    envs.append(f"OSPARC_API_HOST = {scfg[surl]}")
    envs.append(f"OSPARC_API_KEY = {scfg[skey]}")
    envs.append(f"OSPARC_API_SECRET = {scfg[ssecret]}")

    # save client setting (mainly for logging)
    client_settings: List[str] = []
    client_settings.append(f"CLIENT_REPO = {ccfg[crepo]}")
    client_settings.append(f"CLIENT_BRANCH = {ccfg[crepo]}")
    client_settings.append(f"CLIENT_VERSION = {ccfg[crepo]}")

    pytest_settings: Dict[str, Any] = {}
    pytest_settings["env"] = envs
    pytest_settings["client_settings"] = client_settings

    config: Dict[str, Any] = {}
    config["tool"] = {"pytest": {"ini_options": pytest_settings}}

    # generate toml file
    with open(str(ini_file), "w") as f:
        toml.dump(config, f)

    # check client vs server compatibility
    client_ref = ccfg[cbranch] + ccfg[cversion]
    assert (
        client_ref in comp_df.keys()
    ), f"invalid client_ref: {client_ref}.\nValid ones are: {comp_df.keys()}"
    assert (
        osparc_url.netloc in comp_df.index
    ), f"invalid server_url: {osparc_url.netloc}\nValid ones are: {list(comp_df.index)}"

    return comp_df[client_ref][osparc_url.netloc]

if __name__ == "__main__":
    typer.run(main)
