# pylint: disable=protected-access
# pylint: disable=redefined-outer-name
# pylint: disable=too-many-arguments
# pylint: disable=unused-argument
# pylint: disable=unused-variable

import os
import shutil
import sys
from collections.abc import Iterator
from pathlib import Path
from typing import Any, Final

import nbformat
import osparc
import papermill as pm
import pytest
from _utils import (
    RESOURCE_LOG_ENV_VAR,
    delete_recorded_resources,
    read_recorded_resources,
)
from nbconvert.exporters import MarkdownExporter
from packaging.version import Version
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

_HTTP_LOGGING_SETUP_CODE: Final[str] = """
# Injected by test runner: force debug=True on every osparc_client Configuration
import osparc_client
import logging

logging.getLogger("osparc").setLevel(logging.DEBUG)
_orig_init = osparc_client.Configuration.__init__
def _init_with_debug(self, *a, **kw):
    _orig_init(self, *a, **kw)
    self.debug = True
osparc_client.Configuration.__init__ = _init_with_debug
"""

_NOTEBOOK_EXECUTION_TIMEOUT_SECONDS: Final[int] = 60 * 20  # 20min
_docs_dir: Path = Path(__file__).parent.parent.parent / "docs"

all_notebooks: list[Path] = list(_docs_dir.rglob("*.ipynb"))

MIN_VERSION_REQS: dict[str, Version] = {
    "BasicTutorial_v0.5.0.ipynb": Version("0.5.0"),
    "BasicTutorial_v0.6.0.ipynb": Version("0.6.0"),
    "BasicTutorial_v0.8.0.ipynb": Version("0.8.0"),
    "WalletTutorial_v0.8.0.ipynb": Version("0.9.0"),
}


# The notebooks are executed as written and upload a file and submit a job from it with no
# teardown of their own, so the spy that _papermill_execute_notebook prepends reports the ids and
# this fixture deletes them once the notebook is done.
@pytest.fixture
def delete_resources_created_in_notebooks(
    api_client: osparc.ApiClient,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> Iterator[None]:
    # The kernel inherits this from the pytest process. CI points the variable at a path it
    # keeps, so a run that gets killed before this teardown still leaves the ids behind for
    # cleanup_resources.py to find.
    resource_log = Path(
        os.environ.get(RESOURCE_LOG_ENV_VAR) or tmp_path / "resources.jsonl"
    )
    monkeypatch.setenv(RESOURCE_LOG_ENV_VAR, str(resource_log))

    yield

    if recorded := read_recorded_resources(resource_log):
        delete_recorded_resources(api_client, recorded)


def _pretty_print_cell_outputs(notebook_path: Path) -> None:
    """Pretty print the outputs of each cell in the executed notebook."""
    exporter = MarkdownExporter()
    body, _ = exporter.from_filename(str(notebook_path))
    console = Console()
    console.print(
        Panel(
            title=f"Executed notebook {notebook_path.name}", renderable=Markdown(body)
        )
    )


def _notebook_spy_cell() -> str:
    # The kernel runs the same interpreter, so this points it at the suite directory and the spy
    # is imported as the module it is, which keeps it linted and typed, rather than pasted in as
    # a string of code.
    return (
        "import sys\n"
        f"sys.path.insert(0, {str(Path(__file__).parent)!r})\n"
        "import _notebook_spy\n"
        "\n"
        "_notebook_spy.install()\n"
    )


def _inject_setup_cells(notebook_path: Path) -> None:
    # Prepended to the copy the runner executes so they run before any notebook cell: the spy
    # one so a resource gets recorded at the moment the notebook creates it, the logging one
    # so a failed request can be traced by its trace id. The logging cell turns on
    # http.client debugging, which prints every header sent and received; that includes the
    # Authorization header, so it runs only when OSPARC_E2E_HTTP_DEBUG asks for it.
    nb = nbformat.read(notebook_path, as_version=4)
    nb.cells.insert(0, nbformat.v4.new_code_cell(source=_notebook_spy_cell()))
    if os.environ.get("OSPARC_E2E_HTTP_DEBUG"):
        nb.cells.insert(0, nbformat.v4.new_code_cell(source=_HTTP_LOGGING_SETUP_CODE))
    nbformat.write(nb, notebook_path)


def _papermill_execute_notebook(
    tmp_path: Path, notebook: Path, parameters: dict[str, Any]
) -> Path:
    assert notebook.is_file(), (
        f"{notebook.name} is not a file (full path: {notebook.resolve()})"
    )

    if (min_version := MIN_VERSION_REQS.get(notebook.name)) and (
        Version(osparc.__version__) < min_version
    ):
        pytest.skip(
            f"Skipping {notebook.name} because {osparc.__version__=} < {min_version=}"
        )

    tmp_nb = tmp_path / notebook.name
    shutil.copy(notebook, tmp_nb)
    assert tmp_nb.is_file(), "Did not succeed in copying notebook"

    _inject_setup_cells(tmp_nb)

    output: Path = tmp_path / (tmp_nb.stem + "_output.ipynb")

    try:
        pm.execute_notebook(
            input_path=tmp_nb,
            output_path=output,
            kernel_name="python3",
            parameters=parameters,
            execution_timeout=_NOTEBOOK_EXECUTION_TIMEOUT_SECONDS,
        )
    finally:
        _pretty_print_cell_outputs(output)
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
    notebook_names: set = {pth.name for pth in all_notebooks}
    msg: str = (
        f"Must specify max version for: {notebook_names - min_keys}."
        f" The following keys can be deleted: {min_keys - notebook_names}"
    )
    assert min_keys == notebook_names, msg


@pytest.mark.parametrize("notebook", all_notebooks, ids=lambda nb: nb.name)
def test_run_notebooks(
    tmp_path: Path, notebook: Path, delete_resources_created_in_notebooks: None
):
    """Run all notebooks in the documentation"""

    _papermill_execute_notebook(
        tmp_path=tmp_path,
        notebook=notebook,
        parameters={},  # NOTE: for the moment these notebooks have no parameters
    )


def test_http_logging_cell_is_opt_in(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    nb_path: Path = tmp_path / "nb.ipynb"
    nb = nbformat.v4.new_notebook()
    nb.cells.append(nbformat.v4.new_code_cell("print(1)"))
    nbformat.write(nb, nb_path)

    def injected_sources() -> list[str]:
        return [cell.source for cell in nbformat.read(nb_path, as_version=4).cells]

    monkeypatch.delenv("OSPARC_E2E_HTTP_DEBUG", raising=False)
    _inject_setup_cells(nb_path)
    assert not any("debug=True" in source for source in injected_sources()), (
        "the header dump must stay off unless OSPARC_E2E_HTTP_DEBUG is set"
    )

    monkeypatch.setenv("OSPARC_E2E_HTTP_DEBUG", "1")
    _inject_setup_cells(nb_path)
    assert "debug=True" in injected_sources()[0]
