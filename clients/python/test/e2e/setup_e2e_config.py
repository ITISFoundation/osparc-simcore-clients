import toml
from pathlib import Path
import pandas as pd
from urllib.parse import urlparse, ParseResult
from typing import List, Dict, Any
import typer
from packaging import version

def main(
    osparc_server: str, osparc_key: str, osparc_secret: str, client_repo:str, client_branch:str, client_version:str
) -> bool:
    """
    Generates a toml configuration file pytest e2e tests

    returns:
    --------
        A bool indicating whether or not the (client, server) pair are compatible
    """
    # read in data
    osparc_url: ParseResult = urlparse(osparc_server)
    ini_file: Path = Path(__file__).parent / "pyproject.toml"
    ini_file.unlink(missing_ok=True)
    comp_df: pd.DataFrame = pd.read_json(
        Path(__file__).parent / "data" / "server_client_compatibility.json"
    )

    # generate client_ref
    assert (client_repo == "" and client_branch == "") or (client_version == ""), f"client_repo={client_repo}, client_branch={client_branch}, client_version={client_version}"
    assert (client_repo != "" and client_branch != "") or (client_version != ""), f"client_repo={client_repo}, client_branch={client_branch}, client_version={client_version}"
    if client_version != "":
        # raise exception if not valid version
        _ = version.parse(client_version)


    client_ref = client_branch if client_branch != "" else client_version
    assert (
        client_ref in comp_df.keys()
    ), f"invalid client_ref: {client_ref}.\nValid ones are: {comp_df.keys()}"
    assert (
        osparc_url.netloc in comp_df.index
    ), f"invalid server_url: {osparc_url.netloc}\nValid ones are: {list(comp_df.index)}"

    if not comp_df[client_ref][osparc_url.netloc]:
        return False

    # set environment variables
    envs: List[str] = []
    envs.append(f"OSPARC_API_HOST = {osparc_url.geturl()}")
    envs.append(f"OSPARC_API_KEY = {osparc_key}")
    envs.append(f"OSPARC_API_SECRET = {osparc_secret}")

    # save client setting (mainly for logging)
    client_settings: List[str] = []
    client_settings.append(f"CLIENT_REPO = {client_repo}")
    client_settings.append(f"CLIENT_BRANCH = {client_branch}")
    client_settings.append(f"CLIENT_VERSION = {client_version}")

    pytest_settings: Dict[str, Any] = {}
    pytest_settings["env"] = envs
    pytest_settings["client_settings"] = client_settings

    config: Dict[str, Any] = {}
    config["tool"] = {"pytest": {"ini_options": pytest_settings}}

    # finally generate ini file
    with open(str(ini_file), "w") as f:
        toml.dump(config, f)

    return True

if __name__ == "__main__":
    typer.run(main)
