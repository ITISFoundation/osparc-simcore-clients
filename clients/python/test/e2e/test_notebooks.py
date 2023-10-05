import shutil
import sys
from pathlib import Path
from typing import Any, Dict, List

import osparc
import papermill as pm
import pytest
from packaging.version import Version

docs_dir: Path = Path(__file__).parent.parent.parent / "docs"
all_notebooks: List[Path] = list(docs_dir.rglob("*.ipynb"))
max_notebook_versions: Dict[str, Version] = {
    "BasicTutorial_v0.5.0.ipynb": Version("0.5.0"),
    "BasicTutorial_v0.6.0.ipynb": Version("0.6.0"),
}


def test_notebook_config(tmp_path: Path):
    """Checks the jupyter environment is configured correctly"""
    config_test_nb: Path = Path(__file__).parent / "data" / "config_test.ipynb"
    assert config_test_nb.is_file()
    test_run_notebooks(
        tmp_path,
        config_test_nb,
        {
            "expected_python_bin": sys.executable,
            "expected_osparc_version": str(osparc.__version__),
            "expected_osparc_file": osparc.__file__,
        },
    )
    assert len(all_notebooks) > 0, f"Did not find any notebooks in {docs_dir}"
    max_keys: set = set(max_notebook_versions.keys())
    notebook_names: set = set(pth.name for pth in all_notebooks)
    msg: str = (
        "Must specify max version ",
        f"for: {notebook_names-max_keys}.",
        " The following keys can be ",
        f"deleted: {max_keys - notebook_names}",
    )
    assert max_keys == notebook_names, msg


@pytest.mark.parametrize("notebook", all_notebooks)
def test_run_notebooks(tmp_path: Path, notebook: Path, params: dict[str, Any] = {}):
    """Run all notebooks in the documentation"""
    print(f"Running {notebook.name} with parameters {params}")
    assert (
        notebook.is_file()
    ), f"{notebook.name} is not a file (full path: {notebook.resolve()})"
    if Version(osparc.__version__) > Version(max_notebook_versions[notebook.name]):
        msg: str = (
            f"Skipping {notebook.name} because "
            f"{osparc.__version__=} > {max_notebook_versions[notebook.name]}"
        )
        pytest.skip(msg)
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
