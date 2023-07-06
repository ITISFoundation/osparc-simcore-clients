import papermill as pm
from pathlib import Path
from tempfile import TemporaryDirectory
import shutil
import pytest
from typing import List

docs_dir:Path = Path(__file__).parent.parent / 'docs'
all_notebooks:List[Path] = list(docs_dir.glob("*.ipynb"))


@pytest.mark.parametrize('notebook',all_notebooks)
def test_run_notebooks(notebook:Path):
    """Run all notebooks in the documentation
    """
    print(f"Running {notebook.relative_to(docs_dir)}")
    assert notebook.is_file(), f'{notebook.relative_to(docs_dir)} is not a file'
    with TemporaryDirectory() as tmp_dir:
        tmp_nb = Path(tmp_dir) / notebook.name
        shutil.copy(notebook, tmp_nb)
        assert tmp_nb.is_file(), 'Did not succeed in copying notebook'
        output:Path = Path(tmp_dir) / (tmp_nb.stem + '_output.ipynb')
        pm.execute_notebook(input_path=tmp_nb, output_path=output, kernel_name="python")
