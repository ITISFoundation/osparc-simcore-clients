import toml
import typer
from pathlib import Path
from typing import Dict, List
from pprint import pprint

# keys to be found in input dicts
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
    assert len(entries) == 1, f"toml_entry={toml_entry}"
    return entries[0].replace(key, "").strip(" =")


def main(pytest_exit_code: int) -> None:
    """ """
    artifact_dir: Path = Path(__file__).parent.parent.parent / "artifacts" / "e2e"
    cfg_file: Path = Path(__file__).parent / "pyproject.toml"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    assert cfg_file.is_file()

    cfg: Dict = toml.load(cfg_file)["tool"]["pytest"]["ini_options"]
    client_settings: List[str] = cfg["client_settings"]
    assert isinstance(client_settings, list)

    branch: str = extract_val(client_settings, cbranch)
    version: str = extract_val(client_settings, cversion)

    envs: List[str] = cfg["env"]
    assert isinstance(envs, list)

    url: str = extract_val(envs, surl)

    print(branch)
    print(version)
    print(url)


if __name__ == "__main__":
    typer.run(main)
