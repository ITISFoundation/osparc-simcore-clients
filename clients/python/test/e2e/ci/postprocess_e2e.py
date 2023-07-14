import toml
import typer
from pathlib import Path
from typing import Dict, List
import pandas as pd
from urllib.parse import urlparse
import shutil
import json

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
    assert len(entries) == 1, f"toml_entry={toml_entry}"
    return entries[0].replace(key, "").strip(" =")


def main(pytest_exit_code: int) -> None:
    """
    Postprocess results from e2e pytests
    This scripts appends the pytest exit code to clients/python/artifacts/e2e/<client_ref>.json for it to be parsed later
    It also moves the pyproject.toml to clients/python/artifacts/e2e in order to be able to reproduce tests later

    arguments:
    ----------
        pytest_exit_code : Integer exit code from running pytests or -1 which indicates the client and server are incompatible.
                           N.B. -1 doesn't clash with pytest exitcodes: https://docs.pytest.org/en/7.1.x/reference/exit-codes.html

    returns:
    --------
        None
    """
    assert pytest_exit_code in [
        -1,
        0,
        1,
    ], f"Received unexpected pytest exitcode {pytest_exit_code}. See https://docs.pytest.org/en/7.1.x/reference/exit-codes.html"
    return_msg: str
    if pytest_exit_code == -1:
        return_msg = "incompatible"
    elif pytest_exit_code == 0:
        return_msg = "pass"
    else:
        return_msg = "fail"

    artifact_dir: Path = (
        Path(__file__).parent.parent.parent.parent / "artifacts" / "e2e"
    )
    cfg_file: Path = Path(__file__).parent.parent / "pyproject.toml"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    assert cfg_file.is_file(), f"cfg_file={cfg_file}"

    # extract values
    pytest_cfg: Dict = toml.load(cfg_file)["tool"]["pytest"]["ini_options"]
    client_cfg: Dict[str, str] = json.loads(
        toml.load(cfg_file)["client"]["install_cmd"]
    )
    assert isinstance(client_cfg, dict)
    branch: str = client_cfg[cbranch]
    version: str = client_cfg[cversion]
    envs: List[str] = pytest_cfg["env"]
    assert isinstance(envs, list)
    url: str = extract_val(envs, surl)

    # add result to json
    client_ref: str = branch + version
    result_file: Path = artifact_dir / (client_ref + ".json")
    new_df: pd.DataFrame = pd.DataFrame(
        columns=[client_ref], index=[urlparse(url).netloc], data=[return_msg]
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


if __name__ == "__main__":
    typer.run(main)
