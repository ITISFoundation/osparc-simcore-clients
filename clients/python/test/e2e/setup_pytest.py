import toml
from pathlib import Path
import pandas as pd
from urllib.parse import urlparse, ParseResult
from typing import List, Dict, Any
import typer


def generate_pytest_ini(
    client_ref: str, osparc_server: str, osparc_key: str, osparc_secret: str
):
    """
    Generates a toml configuration file pytest e2e tests
    """
    osparc_url: ParseResult = urlparse(osparc_server)
    ini_file: Path = Path(__file__).parent / "pyproject.toml"
    ini_file.unlink(missing_ok=True)

    comp_df: pd.DataFrame = pd.read_json(
        Path(__file__).parent / "data" / "server_client_compatibility.json"
    )
    assert (
        client_ref in comp_df.keys()
    ), f"invalid client_ref: {client_ref}.\nValid ones are: {comp_df.keys()}"
    assert (
        osparc_url.netloc in comp_df.index
    ), f"invalid server_url: {osparc_url.netloc}\nValid ones are: {list(comp_df.index)}"

    # set environmentvaribles
    envs: List[str] = []
    envs.append(f"OSPARC_API_HOST = {osparc_url.geturl()}")
    envs.append(f"OSPARC_API_KEY = {osparc_key}")
    envs.append(f"OSPARC_API_SECRET = {osparc_secret}")

    pytest_settings: Dict[str, Any] = {}
    pytest_settings["env"] = envs

    config: Dict[str, Any] = {}
    config["tool"] = {"pytest": {"ini_options": pytest_settings}}

    # finally generate ini file
    with open(str(ini_file), "w") as f:
        toml.dump(config, f)


if __name__ == "__main__":
    typer.run(generate_pytest_ini)
