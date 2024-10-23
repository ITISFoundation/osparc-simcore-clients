# pylint: disable=protected-access
# pylint: disable=redefined-outer-name
# pylint: disable=too-many-arguments
# pylint: disable=unused-argument
# pylint: disable=unused-variable

import shutil
import sys
from pathlib import Path
from typing import Any, Dict, Final, List

import osparc
import papermill as pm
import pytest
from packaging.version import Version

_NOTEBOOK_EXECUTION_TIMEOUT_SECONDS: Final[int] = 60 * 20  # 20min
_docs_dir: Path = Path(__file__).parent.parent.parent / "docs"

all_notebooks: List[Path] = list(_docs_dir.rglob("*.ipynb"))

MIN_VERSION_REQS: Dict[str, Version] = {
    "BasicTutorial_v0.5.0.ipynb": Version("0.5.0"),
    "BasicTutorial_v0.6.0.ipynb": Version("0.6.0"),
    "BasicTutorial_v0.8.0.ipynb": Version("0.8.0"),
    "WalletTutorial_v0.8.0.ipynb": Version("0.8.3.post0.dev10"),
}


def _papermill_execute_notebook(
    tmp_path: Path, notebook: Path, parameters: dict[str, Any]
) -> Path:
    assert (
        notebook.is_file()
    ), f"{notebook.name} is not a file (full path: {notebook.resolve()})"

    if min_version := MIN_VERSION_REQS.get(notebook.name):
        if Version(osparc.__version__) < min_version:
            pytest.skip(
                f"Skipping {notebook.name} because "
                f"{osparc.__version__=} < {min_version=}"
            )

    tmp_nb = tmp_path / notebook.name
    shutil.copy(notebook, tmp_nb)
    assert tmp_nb.is_file(), "Did not succeed in copying notebook"
    output: Path = tmp_path / (tmp_nb.stem + "_output.ipynb")

    pm.execute_notebook(
        input_path=tmp_nb,
        output_path=output,
        kernel_name="python3",
        parameters=parameters,
        execution_timeout=_NOTEBOOK_EXECUTION_TIMEOUT_SECONDS,
    )
    return output


def test_notebook_config(tmp_path: Path):
    """Checks the jupyter environment is configured correctly"""
    config_test_nb: Path = Path(__file__).parent / "config_test.ipynb"
    assert config_test_nb.is_file()
    _papermill_execute_notebook(
        tmp_path,
        config_test_nb,
        {
            "expected_python_bin": sys.executable,
            "expected_osparc_version": str(osparc.__version__),
            "expected_osparc_file": osparc.__file__,
        },
    )
    assert len(all_notebooks) > 0, f"Did not find any notebooks in {_docs_dir}"
    min_keys: set = set(MIN_VERSION_REQS.keys())
    notebook_names: set = set(pth.name for pth in all_notebooks)
    msg: str = (
        f"Must specify max version for: {notebook_names-min_keys}."
        f" The following keys can be deleted: {min_keys - notebook_names}"
    )
    assert min_keys == notebook_names, msg


@pytest.mark.parametrize("notebook", all_notebooks, ids=lambda nb: nb.name)
def test_run_notebooks(tmp_path: Path, notebook: Path):
    """Run all notebooks in the documentation"""

    _papermill_execute_notebook(
        tmp_path=tmp_path,
        notebook=notebook,
        parameters={},  # NOTE: for the moment these notebooks have no parameters
    )
