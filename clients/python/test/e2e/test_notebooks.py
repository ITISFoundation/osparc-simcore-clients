import json
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

import osparc
import papermill as pm
import pytest

docs_dir: Path = Path(__file__).parent.parent.parent / "docs"
all_notebooks: List[Path] = list(docs_dir.rglob("*.ipynb"))

DOCS_DIR: Path = Path(__file__).parent.parent.parent / "docs"
DATA_DIR: Path = Path(__file__).parent / "data"
TUTORIAL_CLIENT_COMPATIBILITY_JSON: Path = (
    DATA_DIR / "tutorial_client_compatibility.json"
)
API_DIR: Path = DOCS_DIR.parent.parent.parent / "api"

assert DOCS_DIR.is_dir()
assert DATA_DIR.is_dir()
assert TUTORIAL_CLIENT_COMPATIBILITY_JSON.is_file()
assert API_DIR.is_dir()


def _run_notebook(tmp_path: Path, notebook: Path, params: dict[str, Any] = {}):
    """Run a jupyter notebook using papermill

    Args:
        tmp_path (Path): temporary directory
        notebook (Path): path to notebook to run
        params (dict[str, Any], optional): parameters to pass to notebook.
            Defaults to {}.
    """
    print(f"Running {notebook.name} with parameters {params}")
    assert (
        notebook.is_file()
    ), f"{notebook.name} is not a file (full path: {notebook.resolve()})"
    tmp_nb = tmp_path / notebook.name
    shutil.copy(notebook, tmp_nb)
    assert tmp_nb.is_file(), "Did not succeed in copying notebook"
    output: Path = tmp_path / (tmp_nb.stem + "_output.ipynb")
    pm.execute_notebook(
        input_path=tmp_nb,
        output_path=output,
        kernel_name="python3",
        parameters=params,
    )


def _get_tutorials(osparc_version: Optional[str] = None) -> List[Path]:
    """Returns the tutorial notebooks compatible with a given osparc client version

    Args:
        osparc_version (str): osparc.__version__

    Returns:
        List[Path]: A list of *Path*s to the tutorial notebooks
    """
    compatibility_dict: Dict[str, Any] = json.loads(
        TUTORIAL_CLIENT_COMPATIBILITY_JSON.read_text()
    )
    tutorial_names: Set[str] = set()
    if osparc_version is not None:
        assert (
            osparc_version in compatibility_dict["versions"]
        ), f"{osparc_version} does not exist in {TUTORIAL_CLIENT_COMPATIBILITY_JSON}"
        tutorial_names = set(compatibility_dict["versions"][osparc_version])
    else:
        for v in compatibility_dict["versions"]:
            tutorial_names = tutorial_names.union(
                set(compatibility_dict["versions"][v])
            )
    result: List[Path] = []
    for name in tutorial_names:
        result += list(DOCS_DIR.rglob(f"*{name}"))

    return result


# Tests -------------------------------------------------------------------------------


def test_notebook_config(tmp_path: Path):
    """Test configuration of test setup.
    Make sanity checks (ensure all files are discovered,
    correct installations are on path etc)

    Args:
        tmp_path (Path): Temporary path pytest fixture
    """
    # sanity check configuration of jupyter environment
    config_test_nb: Path = DATA_DIR / "config_test.ipynb"
    assert config_test_nb.is_file()
    _run_notebook(
        tmp_path,
        config_test_nb,
        {
            "expected_python_bin": sys.executable,
            "expected_osparc_version": str(osparc.__version__),
            "expected_osparc_file": osparc.__file__,
        },
    )

    # sanity check paths and jsons: are we collecting all notebooks?
    tutorials: Set[Path] = set(DOCS_DIR.glob("*.ipynb"))
    json_notebooks: Set[Path] = set(_get_tutorials())
    assert len(tutorials) > 0, f"Did not find any tutorial notebooks in {DOCS_DIR}"
    assert len(tutorials.difference(json_notebooks)) == 0, (
        "Some tutorial notebooks are "
        "not present in {TUTORIAL_CLIENT_COMPATIBILITY_JSON}"
    )

    # check that version of this repo is present in compatibility json
    current_version: str = json.loads((API_DIR / "config.json").read_text())["python"][
        "version"
    ]
    compatible_versions: Set[str] = json.loads(
        TUTORIAL_CLIENT_COMPATIBILITY_JSON.read_text()
    )["versions"].keys()
    assert current_version in compatible_versions, (
        f"The version defined in {API_DIR/'config.json'} "
        "is not present in {TUTORIAL_CLIENT_COMPATIBILITY_JSON}"
    )


@pytest.mark.parametrize("tutorial", _get_tutorials(), ids=lambda p: p.name)
def test_run_tutorials(tmp_path: Path, tutorial: Path):
    """Run all tutorials compatible with the installed
    version of osparc

    Args:
        tmp_path (Path): pytest tmp_path fixture
        tutorials (List[Path]): list of tutorials
    """
    if tutorial not in _get_tutorials(osparc.__version__):
        pytest.skip(
            (
                f"{tutorial.relative_to(DOCS_DIR)} is not compatible "
                "with osparc.__version__=={osparc.__version__}. "
                "See {TUTORIAL_CLIENT_COMPATIBILITY_JSON.name}"
            )
        )
    _run_notebook(tmp_path, tutorial)
